---
name: api-case-gen
version: "1.2"
description: >
  通用 API 测试设计用例生成器。脚本 + AI 协作模式：脚本从 OpenAPI 规范自动提取
  结构化约束并批量生成基础用例（schema 键 + 正则），AI 负责阅读所有自然语言
  description 补全脚本无法理解的语义约束（字符集、复合规则、条件依赖等）。
  检测参数间条件依赖/值联动/格式约束，输出覆盖正常流、异常流、边界值、参数关联、
  认证校验、分页边界、CRUD 生命周期链的完整测试矩阵，并带响应字段断言。
  脚本做批量，AI 做理解，二者缺一不可，最终实现 100% 约束覆盖。
  当用户提到 API 测试设计、接口用例生成、测试覆盖分析、测试矩阵、接口测试用例时使用。
metadata:
  openclaw:
    emoji: "📋"
    category: testing
    version: "1.2"
    requires:
      bins: ["python3"]
      packages: ["pyyaml>=6.0"]
---

# API Test Case Generator

从 OpenAPI 规范出发，按服务模块逐一分析，生成面向测试执行的设计用例矩阵。

## Design Principles

1. **脚本 + AI 协作** — 脚本做结构化批量提取（schema 键 + 正则），AI 做自然语言语义理解。约束提取率 = 脚本提取 + AI 补全 = 100%
2. **Spec-first** — 直接从规范文件分析，不依赖运行时或 mock，确保 100% 参数覆盖
3. **Modular analysis** — 每个 service/tag 独立分析，粒度契合测试模块划分和 AI 上下文窗口
4. **Deep expansion** — 所有 `$ref` 递归展开至叶子节点，包括嵌套对象、数组 items、跨文件引用
5. **Cross-field awareness** — 自动检测条件必填、值依赖、格式联动、互斥等参数间约束
6. **High signal-to-noise** — slim 模式默认开启，减少低价值重复用例
7. **Measurable coverage** — 输出按优先级分层的用例矩阵，附可量化的覆盖率统计、CRUD 链分析

## Supported Formats

| 格式 | 支持程度 | 说明 |
|------|---------|------|
| Swagger 2.0 单文件 | 完整 | `definitions` + `paths` |
| Swagger 2.0 多文件（service/ + model/） | 完整 | 自动 `$ref` 跨文件解析 |
| OpenAPI 3.0 单文件 | 完整 | `components.schemas` + `requestBody` + `paths` |
| 多文件 + 跨模块引用 | 完整 | 可配置 `ref_version_dirs` 解析策略 |
| JSON / YAML | 完整 | 自动检测格式 |

---

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                    APICaseGenerator                    │
│  (orchestrator — 串联以下组件)                          │
├──────────┬──────────┬──────────┬──────────┬───────────┤
│ Resolver │ Analyzer │Extractor │Generator │ Renderer  │
│          │          │          │          │           │
│ $ref     │ Parse    │ Schema   │ P0/P1/P2 │ Markdown  │
│ 递归展开  │ 参数/模型 │ + Desc   │ 策略生成  │ + YAML   │
│ 跨文件   │ + 响应   │ + 兜底   │ + 跨字段  │ + 覆盖率  │
│ OAS2/3   │ + CRUD   │ + LLM   │ + 认证   │ + CRUD链  │
└──────────┴──────────┴──────────┴──────────┴───────────┘
```

### Extension Points

约束提取器和用例生成策略均为可注册的列表，新增提取模式或场景类型无需改核心代码：

- **`DESC_PATTERNS`** — 描述正则提取规则列表，格式 `(regex, kind, handler, confidence)`，可追加
- **`HINT_KEYWORDS`** — 兜底线索关键词列表，格式 `(regex, label)`，可追加
- **`ENUM_PATTERNS`** — 枚举值提取正则列表，支持中括号/可选值等多种格式
- **`CaseGenerator.generate()`** — 按 P0/P1/P2 分层调用策略方法，可在子类中 override 或追加

---

## Workflow

```
  ┌─────────────┐     ┌─────────────┐     ┌──────────────┐
  │  Phase 1    │────▶│  Phase 2    │────▶│  Phase 3     │
  │  规范解析    │     │  模型展开    │     │  脚本约束提取 │
  │ (OAS2+OAS3) │     │             │     │  (schema+RE) │
  └─────────────┘     └─────────────┘     └──────┬───────┘
                                                 │
                                                 ▼
  ┌─────────────┐     ┌─────────────┐     ┌──────────────┐
  │  Phase 6    │◀────│  Phase 5    │◀────│  Phase 4     │
  │  输出 & 统计 │     │  AI 约束补全 │     │  脚本用例生成 │
  │  + CRUD链   │     │  ★ 必须执行 ★│     │  + slim     │
  └─────────────┘     └─────────────┘     └──────────────┘
```

**核心原则：脚本做结构化提取，AI 做语义理解。二者缺一不可。**

### Phase 1: Spec Parsing

**输入**: 规范文件路径（单文件或多文件目录）

**处理**:
1. 自动检测 Swagger 2.0 (`swagger: "2.0"`) 或 OpenAPI 3.x (`openapi: "3.*"`)
2. Swagger 2.0: 解析 `basePath` + `paths`，参数从 `parameters[].in: body` + `schema.$ref` 展开
3. OpenAPI 3.x: 解析 `servers[0].url` + `paths`，参数从 `requestBody.content.application/json.schema` 展开，响应从 `content.application/json.schema` 提取
4. 跳过 internal API（可配置 `internal_api_key`）

**输出**: `ServiceAnalysis` 列表（每个含 `OperationAnalysis` 列表）

**失败处理**: YAML 解析错误或不可解析的 `$ref` 会记录到日志并跳过对应文件/操作，不会中断全局流程

### Phase 2: Model Expansion

**处理**（对每个操作的每个 body 参数）:
1. 解析 `$ref` 到目标文件，**将 context 切换为目标文件路径**
2. 递归展开 properties 中的 `$ref`（嵌套对象）和 items 中的 `$ref`（数组元素）
3. 循环引用标记 `_circular: true` 后停止（最大深度可配置，默认 8）
4. 一个操作可有多个 body 参数，每个独立展开
5. OpenAPI 3.x: `#/components/schemas/` 引用在当前文件 schemas 中直接解析

**关键设计**: `$ref` 解析上下文随文件切换。如 `A.yaml` 引用 `B.yaml`，B 中的嵌套 `$ref` 以 B 所在目录为基准解析，不回退到 A。

### Phase 3: 脚本约束提取（自动）

脚本从两个结构化来源自动提取约束：

| Layer | 来源 | 置信度 | 能力边界 |
|-------|------|--------|---------|
| **Schema** | YAML 键：`enum`, `maxLength`, `minimum`, `maximum`, `pattern`, `format`, `minItems`, `maxItems` | high | 精确，但大多数中文 API 规范不写这些键 |
| **正则** | 描述中的结构化模式（"不超过N位"、"[A,B,C]"、"范围[M,N]"） | medium | 只能匹配固定句式，覆盖率通常 10-30% |

**脚本的能力天花板**：正则无法理解自然语言。像"只支持大小写字母、数字、英文下划线或者中划线，以字母开头且不能超过32位"这样的复合约束，正则最多提取出"不超过32"，但字符集约束、开头规则都会遗漏。

**这是设计意图**，不是缺陷。脚本负责批量处理能结构化的部分，剩下的交给 AI。

### Phase 4: 脚本用例生成（自动）

基于 Phase 3 提取到的约束，按优先级分层生成：

| 优先级 | 场景类型 | 说明 |
|--------|---------|------|
| **P0** | 正常流（含响应断言）、必填缺失、未认证(401) | 每个接口必有 |
| **P1** | 边界越界、空值、枚举遍历/非法、类型错误、条件必填、格式校验、分页边界 | 依赖约束提取结果 |
| **P2** | 幂等性、路径参数无效 | 通用业务规则 |

slim 模式默认开启（`--no-slim` 关闭）：路径参数无效每接口 ≤1 条，空值仅 required 字段，认证全局 1 条。

CRUD 生命周期链：自动从 operationId 推导，Markdown 顶部输出链表格。

### Phase 5: AI 约束补全（★ 必须执行 ★）

**这是整个 skill 的核心价值所在。**

脚本生成 Markdown 后，你（AI agent）必须执行以下步骤：

#### 5.1 运行 fallback 报告

```bash
python3 api_case_gen.py fallback -d /path/to/v1/ -r /path/to/repo
```

输出所有"有 description 但脚本未能完全提取约束"的字段清单。

#### 5.2 逐字段阅读 description，补全约束和用例

对 fallback 报告中的**每一个字段**：

1. **阅读原始 description 全文**（不是截断的）
2. **用你的语义理解能力判断**：这个 description 里有没有以下约束？
   - 取值范围 / 长度限制
   - 枚举值（即使不是标准格式）
   - 格式要求（日期、JSON、BASE64、文件类型等）
   - 条件依赖（"当 X=Y 时此参数必填/生效"）
   - 字符集约束（"只支持字母数字下划线"）
   - 互斥关系
   - 唯一性要求
3. **对每个发现的约束，生成对应测试用例**，写入对应接口的测试用例表
4. **所有 AI 补充的用例 ID 必须带 `[AI-review]` 前缀**

#### 5.3 处理"无约束"字段

如果一个字段的 description 确实只是简单标签（如"集群ID"、"地域"），确认为"无约束"，不需要补充用例。

#### 5.4 完成标准

**当且仅当 fallback 报告中的所有字段都已处理（补充用例或确认无约束），Phase 5 才算完成。**

不存在"约束提取率 12%"的问题 — 脚本提取 12%，AI 补全剩余 88%，最终覆盖率 = 100%。

### Phase 6: 输出 & 统计

1. **Markdown 测试矩阵** — 每个 service 一份，含 CRUD 链表格 + AI 补充用例
2. **mqapitest YAML**（可选） — 可执行的测试配置，含响应断言
3. **覆盖率统计** — 脚本提取 + AI 补充 = 总覆盖率
4. `auto-supplement` 命令可生成结构化 JSON prompt，用于批量 AI 补充

---

## Usage — 你（AI agent）必须按以下步骤执行

当用户要求生成 API 测试用例时，**严格按 Step 1→2→3 顺序执行，不可跳过任何步骤**。

### Step 1: 运行脚本生成基础用例

```bash
# -r 可省略，脚本会自动从路径推断 repo-root
# 分析单个 service 文件
python3 api_case_gen.py analyze \
  -s /path/to/service/Instance.yaml \
  -o /tmp/cases/

# 或分析整个产品目录
python3 api_case_gen.py analyze-all \
  -d /path/to/product/v1/ \
  -o /tmp/cases/
```

**检查输出**：确认无 `WARNING: Unresolved body $ref` 警告。如有，说明跨模块引用失败，需手动指定 `-r <repo-root>`。

### Step 2: AI 约束补全（★ 不可跳过 ★）

**Step 1 只完成了约 30% 的工作。Step 2 是这个 skill 存在的核心价值。**

脚本正则只能提取结构化模式，大量约束藏在自然语言 description 里，**只有你能理解**。

#### 2.1 打开 Step 1 生成的 Markdown，找到"待 AI 审查"表格

每个接口的 Markdown 里有一个"待 AI 审查（正则未能提取的潜在约束）"表格，列出了脚本检测到有约束线索但无法结构化提取的字段。

#### 2.2 对每个待审查字段，执行以下操作

**逐个字段处理，不允许批量跳过：**

```
对于每个待审查字段:
  1. 用 Read 工具打开该字段所在的原始 YAML 文件
  2. 找到该字段的完整 description（不是 Markdown 中被截断的版本）
  3. 阅读完整 description，判断是否包含以下任一约束：
     □ 取值范围（如"1~30"、"不超过N"）
     □ 枚举值（如"Cluster或Local"、"支持的值为X"、"只有A和B两种"）
     □ 格式要求（如"格式yyyy-MM-dd"、"JSON字符串"、"BASE64编码"）
     □ 字符集（如"只支持字母数字下划线"、"以字母开头"）
     □ 条件依赖（如"当X=Y时必填"、"仅在X模式下有效"）
     □ 互斥 / 唯一性
  4. 对发现的每个约束，生成对应测试用例：
     - 有枚举 → 遍历有效值 + 传非法值
     - 有范围 → 传越界值（上界+1, 下界-1, 0）
     - 有格式 → 传非法格式
     - 有字符集 → 传非法字符（特殊字符、中文等）
     - 有条件依赖 → 满足条件但缺依赖字段 + 不满足条件时传入
  5. 用例 ID 必须带 [AI-review] 前缀
  6. 如果 description 只是纯标签（如"集群ID"），标注"确认无约束"
```

#### 2.3 额外检查：脚本未标记但有隐含约束的字段

除了"待 AI 审查"表格，**还要扫描参数约束摘要中约束列为空或仅有"schema"的字段**。很多字段的 description 里有隐含枚举但脚本没检测到，例如：
- "节点角色 [broker]" → 隐含枚举 [broker]
- "部署模式,Cluster或Local" → 隐含枚举 [Cluster, Local]
- "ACL模式, PLAIN 或 NONE" → 隐含枚举 [PLAIN, NONE]

这些也需要补充枚举遍历 + 非法值用例。

#### 2.4 完成标准

**以下条件全部满足时 Step 2 才算完成：**
1. "待 AI 审查"表格中每个字段都已处理（补充用例或确认无约束）
2. 参数摘要中所有 description 含可选值/范围/格式的字段都已检查
3. 输出最终的完整用例表（脚本用例 + AI 补充用例合并）

**如果你跳过 Step 2 直接输出脚本结果，等于只完成了 30% 的测试设计。**

### CLI 参考（其他命令）

```bash
# 覆盖率统计
python3 api_case_gen.py coverage -d /path/to/product/v1/

# LLM prompt 生成（用于批量补充）
python3 api_case_gen.py auto-supplement -d /path/to/product/v1/ -o prompt.md
```

**注意**：`-r`（repo-root）参数现在可省略，脚本会自动从路径向上搜索包含多个模块目录的根。仅在自动推断失败时需要手动指定。

### Python API

```python
from api_case_gen import APICaseGenerator, AnalysisConfig, detect_crud_chains

config = AnalysisConfig(
    repo_root="/path/to/api-repo",
    output_format="both",
    priority_levels=["P0", "P1"],
    slim_path_params=True,    # 路径参数无效每接口 ≤1
    slim_empty_string=True,   # 空值仅 required 字段
)

gen = APICaseGenerator(config)
results = gen.analyze_product("path/to/product/v1/")

# CRUD 链检测
all_ops = gen.get_all_operations(results)
crud_chains = detect_crud_chains(all_ops)

# 输出
for analysis, cases_by_op in results:
    gen.write_markdown((analysis, cases_by_op), "./cases/", crud_chains=crud_chains)
    gen.write_yaml((analysis, cases_by_op), "./cases/")

gen.print_coverage(results, crud_chains=crud_chains)

# LLM 补充
from api_case_gen import build_llm_supplement_prompt, parse_llm_supplement_response
prompt = build_llm_supplement_prompt(results)
# ... feed prompt to LLM ...
# supplements = parse_llm_supplement_response(llm_response)
```

## Configuration

```yaml
# case-gen-config.yaml

analysis:
  extract_description_constraints: true
  confidence_threshold: medium    # low | medium | high
  max_model_depth: 8              # $ref 递归展开最大深度
  include_internal_apis: false    # 跳过标记为 internal 的 API
  ref_version_dirs: [v1, v2]     # 跨模块 $ref 搜索的版本目录
  internal_api_key: x-jdcloud-internal  # internal 标记键（留空禁用）

generation:
  priority_levels: [P0, P1, P2]
  id_prefix: ""                   # 用例 ID 前缀，空则自动推导

slim:
  path_params: true               # 路径参数无效每接口 ≤1 条
  empty_string: true              # 空值仅 required 字段

output:
  format: both                    # markdown | yaml | both

# 路径参数的环境变量映射（用于 YAML 输出）
env_mapping:
  regionId: "{{env.region}}"
  instanceId: "{{env.instance_id}}"

# 必填参数的测试默认值
defaults:
  regionId: cn-north-1
```

---

## Quality Checklist

### Phase 3-4 完成后（脚本自动）

- [ ] 每个接口至少 1 条 P0 正常流用例（含响应字段断言）
- [ ] 所有 required 参数（含嵌套模型的 required）都有缺失场景
- [ ] 所有 body `$ref` 已递归展开至叶子节点（无残留 `$ref`）
- [ ] 多个 body 参数都已独立展开和生成用例
- [ ] 全局有 1 条未认证（401）用例
- [ ] CRUD 链已识别并输出在 Markdown 顶部

### Phase 5 完成后（AI 必须完成 ★）

- [ ] `fallback` 报告中 **每个字段** 都已处理
- [ ] 有约束的字段：已补充对应 `[AI-review]` 测试用例
- [ ] 无约束的字段：已确认为"纯标签字段"
- [ ] **Pending AI review = 0**（这是 Phase 5 的退出条件）
- [ ] 所有 AI 补充的用例 ID 带 `[AI-review]` 前缀

### 约束覆盖率（脚本 + AI 合计）

- [ ] description 中的枚举值有遍历 + 非法值用例
- [ ] description 中的范围/长度约束有越界用例
- [ ] 参数间条件必填约束有正反两方向用例
- [ ] 日期/格式字段有格式校验用例
- [ ] 文件类型字段有格式/结构校验用例
- [ ] 字符集约束字段有非法字符用例
- [ ] 分页接口有 pageNumber/pageSize 边界用例

---

## NEVER Do

1. **NEVER trust description alone** — description 提取的约束必须标注 `source: description` 和 `confidence`，不直接用于严格断言
2. **NEVER skip fallback review** — 正则提取率通常 < 30%，不审查兜底清单等于放弃大量约束覆盖
3. **NEVER hardcode business values** — 如 regionId、vpcId 等业务值必须通过 config 注入，不写入脚本
4. **NEVER generate empty test suites** — 如果一个接口 0 条用例，说明解析失败，应报错而非静默跳过
5. **NEVER mix auto-generated and manual cases without markers** — AI 补充的用例必须标注 `[AI-review]`

---

## Troubleshooting

| 症状 | 原因 | 解决方案 |
|------|------|---------|
| body 参数显示 0 个属性 | `$ref` 未解析或 model 文件不存在 | 检查 `--repo-root` 路径；运行 `fallback` 查看未解析引用 |
| 约束提取率极低（< 5%） | description 语言非中文，或约束写在操作级描述而非字段级 | 扩展 `DESC_PATTERNS` 添加英文模式，或手动 AI 审查 |
| 跨模块 `$ref` 解析失败 | 相对路径与 repo 目录结构不匹配 | 确认 `--repo-root` 指向仓库根目录，检查版本目录命名 |
| 同名模型字段不一致 | 不同文件中定义了同名 definition | 本工具按 `$ref` 路径精确定位，不会混淆；检查输出确认 |
| 用例数量偏少 | 嵌套模型未充分展开 | 增大 `max_model_depth`（默认 8），检查是否有循环引用 |
| OAS3 requestBody 未解析 | `content` 下非 `application/json` | 当前仅处理 `application/json`，其他 MIME 类型跳过 |

---

## Limitations

1. **OAS3 `oneOf`/`anyOf`/`allOf`** — 不支持 composition 关键字，仅处理 `properties` 和 `$ref`
2. **非 JSON body** — `multipart/form-data`、`application/xml` 等 content type 不处理
3. **Security schemes** — 不解析 OAS3 `securitySchemes`，认证用例为通用 401 检测
4. **Response $ref** — 响应字段仅提取顶层 properties，不递归展开嵌套 `$ref`
5. **描述约束依赖中文模式** — `DESC_PATTERNS` 默认面向中文描述，英文 API 需扩展正则

---

## Changelog

### v1.2 (2026-03-23)

**用例瘦身（Slim mode）**
- 路径参数无效每接口 ≤1 条，自动跳过 regionId/az 等通用参数
- 空值/空数组用例仅对 required 字段生成
- `--no-slim` 可关闭 slim 模式输出全量

**新增测试维度**
- P0 未认证（401）：全局 1 条，网关层统一校验
- P1 分页边界：自动识别 pageNumber/pageSize 参数，生成 0 值/超限用例
- 正常流响应断言：`200, assert: field != null`，YAML 输出含 `body.result.{field} != null`

**CRUD 生命周期链**
- 自动从 operationId 推导 CRUD 链（create/describe/update/delete）
- Markdown 顶部输出链表格，建议端到端测试执行顺序
- Coverage report 输出链统计

**OpenAPI 3.0 完整支持**
- 解析 `requestBody.content.application/json.schema`
- 解析 `#/components/schemas/` 引用
- 解析 `servers[0].url` 作为 basePath
- 响应字段从 `content.application/json.schema` 提取

**LLM 自动补充**
- `auto-supplement` 命令：自动构造结构化 JSON prompt
- `parse_llm_supplement_response()` 解析 LLM 返回结果
- prompt 含 operation_id、description、已提取约束、遗漏线索

### v1.1 (2026-03-22)

- 三层约束提取（schema + description + fallback）
- 参数间约束检测（条件必填、值依赖、格式依赖、互斥）
- 多 body 参数独立展开
- 跨模块 `$ref` 解析（可配置 `ref_version_dirs`）
- 兜底审查报告 + "待 AI 审查"标记
- 覆盖率统计命令

### v1.0 (2026-03-21)

- 初始版本
- Swagger 2.0 多文件解析
- P0/P1/P2 分层用例生成
- Markdown + YAML 输出

---

## Relationship to Other Skills

```
  OpenAPI 规范源文件
        │
        ├─────────────────┬──────────────────────┐
        ▼                 ▼                      ▼
  swagger-skill-python  api-case-gen        api-test-generator
  (合并/查询/调用)      (测试设计矩阵)       (可执行测试配置)
                              │                    │
                              ▼                    ▼
                        设计用例 (.md)         mqapitest YAML
                        + CRUD 链表格          + 响应断言
                        + 覆盖率报告           + 可直接执行
                        + 兜底审查清单
                        + LLM prompt
                              │
                              ▼
                        api-test-converter
                        (格式转换/统一)
```

---

## Caveats

1. **`$ref` 解析上下文切换** — 嵌套 `$ref` 以目标文件所在目录为基准解析，不回退到调用者目录。这是正确行为，但初次接触可能困惑
2. **多 body 参数** — Swagger 2.0 允许一个操作有多个 `in: body` 参数，每个都独立展开和生成用例
3. **兜底检测的误报** — 基于关键词匹配，可能标记实际不含约束的字段。误报无害，漏报才危险
4. **嵌套属性路径** — 用例中引用嵌套字段使用 dot 路径（如 `spec.extension.aclMode`），数组用 `[]` 后缀（如 `items[].nodeCount`）
5. **slim 模式的取舍** — slim 减少低价值用例（空值/路径参数），如需全量覆盖用 `--no-slim`
6. **CRUD 链推导基于命名** — 依赖 operationId 前缀匹配（create/describe/update/delete），非标准命名的接口不会被识别
