# README FOR AI — ai-company 生成与维护规格（独立自包含版）

> **文档性质**：这是给 LLM Agent 阅读的**生成规格**，不是项目介绍。
> 读本文的 Agent 的任务是：**从零生成、再生或扩展 `ai-company` 这个 LLM Agent 治理技能包**，并保持其与本文一致。
>
> **独立性声明（重要）**：`ai-company` 是一个**独立项目**。本文是它的**唯一权威生成规格，完全自包含**——生成/维护本包所需的全部参数、契约、红线、验收项都已内联在本文，**不依赖、不引用任何外部或上层规格文档**。本文任何章节号（如 §9.1）与红线号（如 P21）都是**本地定义**，包内其他文件的 `(README-FOR-AI.md §x.y)` / `P##` 引用一律指向本文。
>
> ⚠️ 本文不参与技能运行时路由。运行时唯一入口是 `SKILL.md`；面向维护仓库的编码 Agent 的简明贡献入口是 `AGENTS.md`。三者职责互斥，不得互相复述内容（见 P55）。

---

## 1. AI-COMPANY 项目与本包定位

AI-COMPANY 是一套**供 LLM Agent 使用的企业治理规范**：把 AI Agent 建模为公司员工，用部门、职能块、错误码、权限边界与升级路径来治理 Agent 行为。它按公司规模分**五档**（该阶梯由本文 §1 本地定义，无需任何外部文档）：

| 档位 | `scale_tier` | major | 部门数 | 职能块 | 结构 |
|---|---|---|---|---|---|
| 微型 XS | `micro` | 1 | 2 | 18 | 扁平（D1+D2） |
| 小型 S | `small` | 2 | 5 | 18 | 扁平 |
| 中型 M | `medium` | 3 | 9 | 18 | 扁平 + 共享模块 |
| 大型 L | `large` | 4 | 18 | 18 | 三层 + 域路由 |
| 集团 G | `group` | 5 | 36 | 36 | 四层 + 总分公司 |

**本包 = 微型档实例**（`ai-company`，v1.0.0）。档位不是单向门：技能可在运行中检测规模溢出、**自主提案**升档，但安装须人工批准（§12）。更高档位的完整结构遵循同一套合并树原则（§10.1），本包当前只实现 `micro → small` 升级边。

**生成任何 AI-COMPANY 包的唯一人工决策是档位**（微型/小型/中型/大型/集团）；本包已锁定**微型**。

## 2. 锁定参数（微型档，生成时逐项对齐，勿跨档混用）

| 参数 | 值 |
|---|---|
| `scale_tier` | `micro`（major = 1，当前版本 `1.0.0`） |
| 部门 | 2：`governance-and-delivery`（前缀 `CEO_`，8 职能块）、`engineering-and-safety`（前缀 `CTO_`，10 职能块） |
| 职能块总数 | **18**（守恒不变量；任何修改后必须复核 `grep -c '^## FB-'` 两文件合计 = 18） |
| 错误码 | **34** = `CEO_001–012` + `CTO_001–012` + `SCL_001–010`（`SCL_` 为基础设施前缀，十条固定，见 §10.3） |
| triggers | **15** 条，3 组（治理 6 / 工程 5 / 交付 4）；含固定 2 条升级（`evaluate scaling threshold`、`propose tier upgrade`）+ 1 条语言（`respond in user language`）；全小写任务语义短语 |
| frontmatter | ≤ **85** 行；`permissions` 块逐字符照抄 §9.1，**任何情形不得改动** |
| SKILL.md 正文 | ≤ **120** 行，只含 §6.2 白名单 8 类内容 |
| 治理与社区文件 | **13** 个（含 `AGENTS.md`），全档位统一不裁剪 |
| prompts | **2** 个，均 `human-paste`（升 small 档时自动新增 `03-test-cases.md`，`agent-invoked`） |
| 执行引擎触发器 | 微型档仅 `Manual` + `Schedule`（4 种执行模式 Auto/Approve/Review/Hybrid 全档有效） |
| WFT 核心集 | 微型档启用 WFT-001 / WFT-002 / WFT-010（3 个） |
| 文件总数 | **25**（见 §4） |
| 记忆系统 / 熔断 / 董事会阶梯 / 域路由 / 模型管理 / 可视化 / 数据集成 | 微型档**不引入**（M+ 或 L+ 档启用）；D2 中以 "at M+/L+ tiers" 限定语承载相应职能语义 |

## 3. 文件树（25 文件，结构须与磁盘始终一致）

```text
ai-company/
├── .editorconfig              # 编辑器统一行为（LF、UTF-8、缩进；[*.ps1] CRLF）
├── .gitignore                 # 通配排除（REVIEW-*.md、__pycache__/、.skill-upgrade/…）
├── .scaling-state.json        # 升级状态（tier_history 只追加）
├── AGENTS.md                  # 编码 Agent 贡献入口（≤150 行，零内容复制，P55）
├── CHANGELOG.md               # Keep a Changelog 格式
├── CODE_OF_CONDUCT.md         # Contributor Covenant 2.1
├── CONTRIBUTING.md            # 分支/提交/测试/验收规则
├── LICENSE                    # GPL-3.0 全文（四处许可同值）
├── README-FOR-AI.md           # ★ 本文：独立自包含生成规格（ASCII 序 '-' < '.'，故在 README.en.md 前）
├── README.en.md               # 与 README.md 相同的英文副本（语言后缀对称）
├── README.md                  # 人类主入口（结构树与磁盘逐项一致）
├── README.zh.md               # 中文版（标识符六类不译，见 §6.3）
├── SECURITY.md                # 版本范围/上报渠道/披露时限/安全底线
├── SKILL.md                   # ★ 技能运行时唯一入口（frontmatter + ≤120 行正文）
├── _meta.json                 # 安装器元数据（major = 档位序号）
├── prompts/
│   ├── 01-implement-method.md     # human-paste（自包含，H1–H7）
│   └── 02-robustness-checks.md    # human-paste（自包含，H1–H7）
├── references/
│   ├── method-patterns.md     # ★ 代码唯一权威源：10 模板 + 3 框架 + 合规段
│   ├── error-codes.md         # 34 条四要素全表
│   ├── scaling.md             # 升级规格：阈值/拆分/六门/别名/降级
│   └── departments/
│       ├── governance-and-delivery.md   # D2，8 FB
│       └── engineering-and-safety.md    # D2，10 FB
├── scripts/
│   ├── self-scale.ps1         # 自我升级脚本（propose-only，六道门）
│   └── scaling-config.json    # 升级配置（阈值/不可变路径）
└── tests/
    └── test-method-patterns.py  # 四类断言 A/B/C/D，24 条
```

> 25 = 治理层 13 + `.scaling-state.json` 1 + `README-FOR-AI.md`（本文）1 + prompts 2 + references 顶层 3 + 部门 D2 2 + scripts 2 + tests 1。升 small 档为 **29**（−2 旧 D2 +5 新 D2 +1 新 prompt = +4）。

## 4. 从零再生本包的工作流（内容依赖顺序）

| Step | 产出 | 关键约束（章节均指本文） |
|---|---|---|
| 0 | 锁定档位 | 微型（本包已锁；新建包时先问人工，无答复默认小型） |
| 1 | 锁定参数 | 照抄 §2 表 + §10.1 合并树，不得自创部门/slug/前缀 |
| 2 | 建目录 + `.scaling-state.json` | 先建目录；状态文件规格见 §12.6 |
| 3 | `references/method-patterns.md` | 10 模板签名逐字符照抄 §7.1；`mask_sensitive_data` 必含 EMAIL/IP/PHONE 三类；7 章节结构（§7.3） |
| 4 | `references/error-codes.md` | 编号连续无空洞；`SCL_` 十条 Message 与 §10.3 逐字符一致；四要素表 |
| 5 | 2 个部门 D2 | 骨架照 §10.2；每 FB 含 3–7 节；职责条目四要素；职能不丢失（对照 §10.1 血统） |
| 6 | `prompts/` 2 个 | 首屏骨架照 §11.4；human-paste 满足 H1–H7（§11.2） |
| 7 | 升级四件套 | `scaling.md` + `self-scale.ps1` + `scaling-config.json` + 状态文件；propose-only；六道门（§12） |
| 8 | `tests/` | 四类断言照 §13 |
| 9 | `SKILL.md` + `_meta.json` | frontmatter 逐字段照 §6.1（≤85 行）；正文 ≤120 行白名单内容 |
| 10 | 13 个治理文件 | 按文件树 ASCII 顺序（`.editorconfig` → … → `SECURITY.md`）；`AGENTS.md` 首屏职责声明 + ≤150 行 |
| 11 | 本文 `README-FOR-AI.md` | 独立项目的生成规格 |
| 12 | 自检 | 跑 §15 验收清单，全部通过才算完成（P39） |

## 5. 硬规则速览（完整清单见 §14 的 P1–P55）

| 规则 | 红线 | 一句话 |
|---|---|---|
| 代码只存一处 | P10/P44 | 模板代码只在 `method-patterns.md`；任何文件不得内联复制 |
| 部门子目录不放 SKILL.md | P1 | 防被加载器误注册为独立技能 |
| 职能块守恒 | P6/P33 | 修改后 `## FB-N:` 合计必须仍 = 18 |
| SKILL.md 只做索引 | P43 | 不放代码/完整错误码表/SOP |
| 权限块不可改 | P21/P22 | `permissions` 逐字符不变，即使升级/人工批准 |
| 升级只提案不自装 | P34–P36 | `self-scale.ps1` 无 install/apply/commit 取值 |
| human-paste 自包含 | P46 | 不得引用内部路径/标识符 |
| 语言分离 | P47/P48 | 源文件英语；输出跟随用户；标识符六类永不译 |
| 治理文件不裁剪 | P50/P53 | 13 个全档位齐备；不建空占位 |
| AGENTS.md 不复述 | P55 | 单向引用零内容复制，不成为第二入口 |
| 无硬编码路径 | P18 | 一律 `{SKILL_DIR}`/`{WORKSPACE_ROOT}` 占位符或相对推导 |
| 数量宣称与磁盘一致 | P4 | "N 个部门/模板/文件" 必须实测相符 |

---

## 6. SKILL.md 规格

### 6.1 frontmatter（逐字段；总行数 ≤85）

```yaml
---
name: "ai-company"     # 单行引号标量，禁用 | 或 > 块标量（P15）
slug: "ai-company"
version: "1.0.0"                  # major = 档位序号（micro=1）
description: "<700–900 字符英文一段话：档位/2 部门/18 职能块/共享资产/双模式 prompts/语言策略/自我升级/何时使用>"
license: "GPL-3.0"
author: "AI Company Team"
tags: [<8–16 个标签>]
dependencies: []                  # 恒为空数组
triggers:                         # 15 条，3 组；见 §2
  - ...
interface:
  inputs:
    type: object
    schema:
      type: object
      properties:
        task: { type: string, description: Task description }
        department:               # 微型档内联 enum（≤9 项 + auto）
          type: string
          enum: [auto, governance-and-delivery, engineering-and-safety]
          description: Which department to invoke; omit or "auto" to auto-route
        output_language: { type: string, description: Override runtime output language }
        context: { type: object, description: Optional context information }
      required: [task]
  outputs:
    type: object
    schema:
      type: object
      properties:
        result: { type: string, description: Operation result }
        report: { type: object, description: Detailed report data }
      required: [result]
  errors: []                      # 全表在 references/error-codes.md，此处留空（P17）
error_code_prefixes: [CEO_, CTO_, SCL_]   # 只列前缀，不列具体码
language_policy:                  # 全档位必备，见 §6.3
  authoring: en
  encoding: utf-8
  output: user-specified
  fallback: en
  immutable_tokens: [slug, error_code, field_name, enum_value, file_path, function_name]
self_scaling:
  enabled: true
  state_file: .scaling-state.json
  spec: references/scaling.md
  upgrade_policy: propose-only    # 只能是 propose-only（P36）
  max_tier: group
permissions:                      # ★ 逐字符照抄 §9.1，永不变
  files:
    read:  ["{WORKSPACE_ROOT}/**", "{SKILL_DIR}/**"]
    write: ["{WORKSPACE_ROOT}/**"]
    deny:  ["~/.ssh/**", "~/.aws/**", "~/.config/**", "/etc/**", "{WINDOWS_DIR}/**"]
  network: []
  commands: []
  mcp: [sessions_send, subagents]
quality:
  idempotent: true
metadata:
  category: enterprise
  layer: AGENT
  cluster: governance
  maturity: STABLE
  license: GPL-3.0
  standardized: true
  scale_tier: micro               # 档位决策留痕（P31）
  department_count: 2
  function_block_count: 18
  harness_baseline: L3            # 交付下限（§8.2）
---
```

`_meta.json`：`{ "ownerId": "ai-company", "slug": "ai-company", "version": "1.0.0", "license": "GPL-3.0", "publishedAt": <epoch_ms> }`。四处版本号（`_meta.json` / README badge / frontmatter / 正文标题）与四处许可（LICENSE / frontmatter / `_meta.json` / metadata）必须同值（P11）。

### 6.2 正文白名单（≤120 行；出现黑名单内容即不合格，P43）

**只允许 8 类**：① 一句话定位（≤3 行）② 域索引（微型档**无**）③ 部门索引表（2 部门各 1 行：slug / 前缀 / 一句话职能 / D2 链接）④ 共享资源速查（指向 method-patterns / error-codes / scaling 的链接表）⑤ 错误码**前缀**清单（只列前缀与含义，不列具体码）⑥ prompts 双模式索引（文件名 / mode / 一句话用途）⑦ 快速上手 3–5 步 ⑧ frontmatter。

**黑名单**（应移至对应文件）：任何代码实现 → method-patterns.md；完整四要素错误码表 → error-codes.md；SOP/处置步骤 → 部门 D2；部门职责正文（超一句话）→ D2；升级阈值/门控/别名表 → scaling.md；提示词框架全文 → method-patterns.md；与实际不符的数量宣称（P4）。

**索引硬要求**：零孤儿（references 与 prompts 下每个 .md 被引用至少一次，P8）；零断链（相对链接目标真实存在）；数量宣称与磁盘一致（P4）。

### 6.3 语言策略与源文件标准（R3-4）

- **编译语言（源文件）= 计算机标准语言**：英语；标准语法；UTF-8 无 BOM；代码块用带语言标识的围栏（```` ```python ````，禁裸围栏）；ISO 8601 带时区；SPDX 许可标识。中英混排仅限既有术语注释。
- **输出语言 = 用户指定语言**：由运行期判定链决定（用户显式 > 任务上下文 > `fallback: en`）；**源文件不得写死输出语言**（P47）。
- **六类标识符永不翻译**（P48）：slug / 错误码 / 字段名 / 枚举值 / 文件路径 / 函数名。`README.zh.md` 尤其易犯。

---

## 7. 代码模板与提示词框架（唯一权威源 = `references/method-patterns.md`）

### 7.1 十个共享模板（签名逐字符固定；参数名与默认值不得改）

| # | 签名 | 用途 | 安全约束 | Harness |
|---|---|---|---|---|
| 1 | `validate_input_schema(data, schema)` | Schema 校验 | 无外部 I/O | L2 |
| 2 | `sanitize_user_query(query)` | 输入净化 | 无动态代码执行 | L3 |
| 3 | `execute_safe_command(cmd, timeout=30)` | 沙箱执行 | 超时 + 受限 cwd | L4 |
| 4 | `format_output_json(content, provider)` | 标准 JSON + AIGC 标签 | 内嵌 AI 水印 | L5 |
| 5 | `retry_with_backoff(func, max_retries=3)` | 指数退避 | 容错 | L3 |
| 6 | `read_reference_file(filepath)` | 安全读文件 | 路径校验，越界拒绝 | L3 |
| 7 | `generate_trace_id(prefix="trace")` | 审计追踪 ID | 无状态 | L5 |
| 8 | `check_rate_limit(identifier, limit=10, window=60)` | 限流 | 仅内存，不落盘 | L4 |
| 9 | `mask_sensitive_data(text)` | PII 脱敏 | 不记录原始数据 | L5 |
| 10 | `build_prompt_from_template(template, **kwargs)` | 提示词生成 | 输入先净化 | L3 |

**模板 9 的完整实现（三类脱敏，缺一不可；P32 教训）**——占位符固定 `[EMAIL]`/`[IP]`/`[PHONE]`：

```python
def mask_sensitive_data(text):
    """Mask sensitive information in output (emails, IPs, phone numbers)."""
    # Mask email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL]', text)
    # Mask IP addresses
    text = re.sub(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', '[IP]', text)
    # Mask phone numbers (11-digit)
    text = re.sub(r'\b[0-9]{11}\b', '[PHONE]', text)
    return text
```

### 7.2 三个提示词框架（逐字符照抄）

```text
CRISPE（复杂任务，6 段）:
[Role] {role_description}
[Result] {desired_output}
[Input] {input_data}
[Steps] {step_by_step}
[Parameters] {constraints}
[Example] {example}

3WEH（清晰委派，4 段）:
Who: {role}
What: {task}
Why: {purpose}
How: {format_constraints}

Five-Element（企业合规，5 段）:
Role: {role}
Task: {task}
Context: {context}
Format: {output_format}
Constraint: {constraints}
```

框架的逐字段展开**只存在于** `method-patterns.md` 第 4 节；`SKILL.md` 只写框架名 + 链接。

### 7.3 method-patterns.md 结构与单一权威源验收

七章节：`## 1. Template Index` / `## 2. Prompt Framework Index` / `## 3. Shared Code Templates`（10 模板完整代码）/ `## 4. Prompt Frameworks (Full)` / `## 5. Compliance Verification` / `## 6. Constraints` / `## 7. Department-Specific Patterns`（微型档写 "L/G tiers only; not applicable at micro tier"，标题保留）。

验收：10 个 `def <fn>` 齐全；含 `[PHONE]`；`references/templates.md` **不存在**；全包每个 `def <fn>` **恰 1 处**命中（P10/P44 复发信号）；代码块全 ```` ```python ````。

---

## 8. Harness 成熟度

### 8.1 L1–L6 分级（不得改级定义；`T<n>` = §7.1 模板编号）

| 级 | 名称 | 必备构件（累加） | 可交付 |
|---|---|---|---|
| L1 | Skeleton | frontmatter 合规 + schema 声明 | ❌ |
| L2 | Functional | + 输入校验(T1) + 输出格式化(T4) | ❌ |
| **L3** | Robust | + 错误处理 + 重试(T5) + **幂等** | ✅ **交付下限** |
| L4 | Resilient | + 限流(T8) + 熔断 + 超时 + 监控 | ✅ |
| L5 | Compliant | + AIGC 三重标识(T4) + PII 脱敏(T9) + 审计追踪(T7) | ✅ |
| L6 | Certified | + STRIDE + CVSS + CISO 签核 | ✅ |

### 8.2 交付下限与声明位置

- **累加性**：L4 必含 L3 全部构件；**不得跳级声明**（声称 L5 却无幂等实现按 L2 计并记缺陷）。
- **交付下限 L3**：任何写入交付物的能力单元不得低于 L3；面向客户（产出离开本组织）不得低于 L5。
- **声明位置**：每个部门 D2 引言块声明 `Department Harness Baseline: L3`；每个职能块 `### 7. Quality Metrics` 首行声明 `Harness Level: L<n>`（n≥3）。声明级别高于可查证据即违反 P49/P24。
- 三层错误恢复（L4 必备）：操作级指数退避 → 事务级回滚（禁先删后恢复，P23）→ 服务级熔断（CLOSED→OPEN→HALF_OPEN）。

### 8.3 幂等

所有操作可安全重试（`quality.idempotent: true`）；非幂等操作不得自动重试。

---

## 9. 安全与合规不变量（任何档位不得裁剪）

### 9.1 权限声明（逐字符照抄；⚠️ 自我升级也不得改动）

```yaml
permissions:
  files:
    read:  ["{WORKSPACE_ROOT}/**", "{SKILL_DIR}/**"]
    write: ["{WORKSPACE_ROOT}/**"]
    deny:  ["~/.ssh/**", "~/.aws/**", "~/.config/**", "/etc/**", "{WINDOWS_DIR}/**"]
  network: []
  commands: []
  mcp: [sessions_send, subagents]
```

- 写权限**严格限于** `{WORKSPACE_ROOT}`；技能目录 `{SKILL_DIR}` 自身**只读**（P21）。
- `deny` 5 项**不得删减任何一项**（P22，P0 级安全边界，微型档也不例外）。
- 一律用 `{WORKSPACE_ROOT}`/`{SKILL_DIR}`/`{WINDOWS_DIR}` 占位符，**禁硬编码绝对路径**（P18）。
- `network`/`commands` 在根清单恒空；子技能如需网络能力在自己的 D2/D3 声明，不改根清单。
- ⚠️ **自我升级不构成放宽本条的理由**：§12 的三段式架构正是为在保持本条不变的前提下实现升级而设计。

### 9.2 AIGC 三重标识（缺一即不合规）

| # | 层 | 载体 | 形态 |
|---|---|---|---|
| 1 | 显式标签 | 内容可见处 | `> ⚠️ AI-Generated Content` 或等价声明 |
| 2 | 隐式元数据 | 结构化输出 | `"ai_generated": true`、`"generated_at": "<ISO8601>"`、`"model": "<provider/model>"` |
| 3 | 内嵌水印 | 内容本体 | 由 `format_output_json`(T4) 注入，不可被简单删除 |

### 9.3 PII 脱敏强制

`mask_sensitive_data`(T9) 在**所有输出管道**强制启用；**EMAIL/IP/PHONE 三类齐全**（缺一即缺陷，P32）；脱敏**先于**任何落盘/日志/外发；原始数据不得记入日志。

### 9.4 安全底线（不可协商）

- **零动态代码执行**：无 `eval`/`exec` 处理用户输入；无 `Invoke-Expression`/`iex`/`DownloadString`（P25）。
- **零硬编码密钥**：一律走环境变量，配置只写变量名不写值——连"示例密钥"也不行（P20）。
- **零敏感路径访问**：`deny` 5 项主动排除。
- **零自我改写**：技能不得写入 `{SKILL_DIR}`（P21/P36），见 §9.5。
- **幂等**：所有操作可安全重试（§8.3）。
- **回滚不得先删后恢复**：`Copy-Item` 到临时目录 → 校验 → 原子替换 → 确认成功后才删旧（P23）。

### 9.5 ⚠️ 三件绝不可自我修改的东西（即使人工批准也不得放行）

| # | 不可修改项 | 后果 | 门 | 错误码 |
|---|---|---|---|---|
| 1 | `permissions` 块（含 write 范围与 deny 5 项） | 自我提权：可给自己加 `{SKILL_DIR}` 写权限、删 deny 项 | G1/G3 | `SCL_004` |
| 2 | `tests/**` 全部文件 | 自我豁免：可改验收期望值掩盖缺陷 | G2 | `SCL_005` |
| 3 | `scripts/self-scale.ps1` 门控逻辑 | 可关闭自己的安全门 | G3 | `SCL_004` |

人工批准的对象是**业务规模变更**，不是**安全边界变更**；安全边界变更须通过重新生成本规格 + 人工审计。

---

## 10. 部门与错误码

### 10.1 合并树、职能块守恒与微型档职能块花名册

**核心不变量**：大档任一部门 = 小档某部门拆出的若干原子部门之并；升级时按合并树**机械拆分**，不需自由发挥。职能块守恒：XS/S/M/L 档恒 = **18**，G 档 = 36（升级门 G4 判据）。

微型档 18 个职能块（`## FB-N: <ROLE>`）的血统与归属：

```text
governance-and-delivery (CEO_, 8 FB)
  FB-1 CEO   ← executive-office + strategy-planning（战略/愿景/危机/OKR/路线图/市场进入/高管沟通）
  FB-2 COO   ← operations-command + hq-coordination（SLA/资源调度/PDCA/跨 Agent 路由/审计追踪；message-bus 语义 M+ 档）
  FB-3 BRD   ← board-governance（升级阶梯/授权矩阵/股东报告；board tier L+ 档）
  FB-4 CFO   ← financial-management + treasury-budget（预算/定价/财务分析/现金流/资本支出）
  FB-5 CRO   ← risk-management + internal-audit（FAIR/熔断/风险阈值 + 内部审计/财务合规/证据链）
  FB-6 PRC   ← procurement-vendor + billing-unit-economics（采购/供应商/合同成本/计费/单位经济）
  FB-7 CQO   ← quality-assurance + information-services 的融合职能（质量门/测试/DORA/文档完整性/多源信息融合）
  FB-8 INFO  ← project-management + localization-translation（项目排期/冲刺承诺/工单 SLA/客户升级/翻译/文化适配）

engineering-and-safety (CTO_, 10 FB)
  FB-1 CTO   ← engineering-architecture + developer-tooling（架构/Agent 创建/部署门 + 内部工具/SDK/开发者体验/模板库）
  FB-2 FW    ← platform-framework（框架标准/CI-CD/Harness/ADR/脚手架）
  FB-3 MDL   ← model-management + data-engineering（模型注册表/调用策略/适配器 + 数据管道/schema/多源融合）
  FB-4 CISO  ← security-operations + resilience-continuity（STRIDE/CVSS/安全门/渗透测试 + 业务连续性/灾备/RTO-RPO）
  FB-5 CLO   ← legal-compliance + privacy-data-protection（法律/AIGC 合规/DMCA/知识产权 + PII/GDPR-PIPL-CCPA/数据驻留）
  FB-6 IRP   ← incident-response + identity-access（安全事件生命周期/取证/通报 + 认证/授权/凭据/mTLS/最小权限）
  FB-7 CHO   ← agent-lifecycle + capability-training（Agent 入职离职/编制/技能差距 + 培训/认证/能力矩阵）
  FB-8 KNM   ← knowledge-management + ethics-culture（知识提取/学习管道/记忆治理[M+ 档] + 伦理审查/文化审计/举报机制）
  FB-9 CMO   ← marketing-brand + partnerships-ecosystem（品牌/GTM/NPS/内容 + 合作/生态/渠道/联盟）
  FB-10 INTEL← competitive-intelligence + sentiment-analysis 基础职能（情报循环/SITREP/情报库/来源可靠性；不含 G 档 D4 引擎）
合计 8 + 10 = 18 ✓
```

**前缀继承**：合并后采用上位部门前缀，被合并部门前缀在该档退役（`references/error-codes.md` 每档只列启用前缀）。升级时退役前缀复活并从 `001` 重新起编。

**micro → small 拆分**（升级用）：`governance-and-delivery` → `governance-and-operations`(6) + `quality-and-delivery`(2)；`engineering-and-safety` → `technology-and-platform`(3) + `security-and-compliance`(3) + `people-and-growth`(4)。

### 10.2 部门 D2 索引页骨架（所有部门统一；变体数必须 = 1）

```markdown
# <Department Display Name>

> Function blocks: <N>                    ← 合并档位必填，守恒校验用
> Department Harness Baseline: L3          ← 必填（§8.2）

## 1. Trigger Scenarios        ← 5–10 条自然语言任务描述
## 2. Core Identity            ← 角色定位、权限边界、汇报关系（微型档无"所属域"）

## FB-1: <ROLE>                ← 每个职能块重复以下 5 节
### 3. Core Responsibilities   ← 每条含【职责描述 + 输入 + 输出 + SLA】四要素
### 4. Error Codes             ← 该 FB 相关错误码四要素表（与 error-codes.md 同码同文）
### 5. Integration Points      ← 与哪些部门协作、通过什么机制
### 6. Constraints             ← 禁止事项，❌ 列表
### 7. Quality Metrics         ← 首行 Harness Level: L<n>（n≥3），其后可量化指标 + 阈值

## FB-2: <ROLE2>               ← 下一个职能块，重复 3–7 节
...
```

微型档**无** `## Prompts` / `## Workflows` 段（那是 L/G 档）。章节编号从 1 起不跳号（P5）；职能块标题严格 `## FB-<N>: <ROLE>`（P40）。

### 10.3 错误码规则

- 命名 `<PREFIX>_<NNN>`，三位零填充，从 `001` 起，**连续无空洞**（P14）；新增追加末尾不插中间。
- 微型档 34 条：`CEO_001–012`、`CTO_001–012`、`SCL_001–010`。
- 每条**四要素**：`| Code | Message | Trigger Condition | Resolution Steps |`。四要素表只存在于 `error-codes.md` 与部门 D2；`SKILL.md` 只列前缀。
- D2 各 FB 的 `### 4` 与 `error-codes.md` 全表**同码同文**；每个部门码恰归属一个 FB。

**`SCL_` 十条（全档位固定，Message 逐字符照抄）**：

```text
SCL_001 Upgrade threshold not met
SCL_002 Upgrade path undefined in merge tree
SCL_003 Alias collision detected
SCL_004 Permission self-modification attempted
SCL_005 Test self-modification attempted
SCL_006 Upgrade package validation failed
SCL_007 Scaling state file corrupted
SCL_008 Downgrade requires manual approval
SCL_009 Tier already at maximum (group)
SCL_010 Function block conservation violated
```

### 10.4 部门 slug 命名规范

全小写 ASCII + 连字符，无空格/下划线/点号；≤40 字符；首尾为字母；缩写白名单仅 `hq mlops aigc iam viz dx gdpr`，其余全拼；全包唯一；不加域前缀；永为英语不翻译（P27/P48）；一旦发布永久保留为别名（§12.4）。

---

## 11. prompts 双模式

### 11.1 两种模式与对称性

| 模式 | 标识 | 消费者 | 核心要求 |
|---|---|---|---|
| 人工粘贴 | `mode: human-paste` | 人类 → 任意 AI 对话窗口 | **自包含**：不引用本技能任何内部路径/文件名/slug |
| Agent 调用 | `mode: agent-invoked` | 本技能内 Agent 自动加载 | 可用 `{SKILL_DIR}` 占位路径、锚点、错误码、工具声明 |

微型档 2 个 prompt 均为 `human-paste`（`01-implement-method.md`、`02-robustness-checks.md`）。命名 `<两位序号>-<kebab-case>.md`，序号全档位一致不因裁剪重编号。零孤儿：每个 prompt 被 `SKILL.md` 的 Prompts 索引列出（含 mode 列）。

### 11.2 human-paste 七条强制约束（H1–H7）

H1 零内部路径（不出现 `references/`、`prompts/`、`scripts/`、`{SKILL_DIR}`、`SKILL.md`、`method-patterns`）；H2 零内部标识符（不出现部门 slug、错误码、`FB-N`、`WFT-NNN`）；H3 背景内联（自带足够规范摘要，如 10 模板签名清单 + 三类脱敏占位符 + AIGC 三重标识要求）；H4 填空位用 `<尖括号>` 且顶部列"使用前需填写"清单；H5 输出契约明确；H6 语言中立（含"以你当前对话所用语言输出"，**不得**写死 English）；H7 平台中立（不提任何 Agent 产品名）。

### 11.3 agent-invoked 五条强制约束（A1–A5，升档新增 03 时用）

A1 路径用占位符（`{SKILL_DIR}`/`{WORKSPACE_ROOT}`，禁硬编码）；A2 声明期望产物（产出哪些文件、写入哪）；A3 声明失败错误码；A4 声明 Harness 级别（≥L3）；A5 引用而非复制（模板写锚点 `method-patterns.md#3-9-mask_sensitive_data`，禁内联代码）。

### 11.4 prompt 首屏骨架（逐字符照抄）

```markdown
---
mode: human-paste            # 或 agent-invoked
id: 01-implement-method      # 与文件名主干一致
title: Implement Method      # 英语
output_language: user-specified
harness_level: L3
---

> **模式**：人工粘贴（human-paste）
> **用途**：复制到任意 AI 对话窗口，让该 AI 按本规范实现一个方法。
> **本文件不由 Agent 自动调用。**
>
> **使用前需填写**：
> - `<METHOD_NAME>` — 要实现的方法名
> - `<LANGUAGE>` — 目标编程语言
> - `<CONSTRAINTS>` — 项目特定约束
>
> **输出语言**：跟随你当前对话所用的语言。

## Prompt
（以下整块可复制）
## 期望输出
## 自检清单
```

`agent-invoked` 差异：`mode` 值不同；去掉"使用前需填写"与"本文件不由 Agent 自动调用"；增加"期望产物路径""失败错误码""引用的模板锚点"三项。

---

## 12. 自我升级机制

### 12.1 三段式架构（技能只提案，不自装）

```text
① 提案 Propose   技能自己完成：检测阈值 → 生成升级包到 {WORKSPACE_ROOT}/.skill-upgrade/<ts>/ → 跑六道门 → 出报告 → 停止
② 批准 Approve   人工审阅报告后批准（唯一人工门）
③ 安装 Install   外部受信任安装器执行（技能永不安装，P36）
```

`self-scale.ps1` 的 `param` 只有 `evaluate`/`propose`/`report`/`status`——**无 install/apply/commit 取值**。

### 12.2 四类触发阈值（微型档值；写入 scaling.md 与 scaling-config.json）

| 触发器 | 量化条件（micro） | 数据来源 |
|---|---|---|
| T1 Agent 规模溢出 | Agent 数 > 3 | `.scaling-state.json` `last_metrics.agent_count` |
| T2 职能块过载 | 单部门职能块 > 均值×1.5 = 9.0×1.5 = **13.5**（≥14 溢出） | D2 页 `^## FB-\d+:` 计数 |
| T3 路由准确率下降 | `department: auto` 命中率 < 85%，连续 3 次 | 运行日志聚合 |
| T4 错误码复用率过高 | 单前缀下不同职能共用同码比例 > 25% | error-codes.md 分析 |

任一命中 → 自主生成提案（不自动安装）；全部未命中 → 更新 `next_evaluation`（默认 +30 天）与 `last_metrics`。阈值必须可量化（禁"视情况评估"）。

### 12.3 六道升级安全门（实现什么写什么，P24）

| # | 门 | 检查 | 失败错误码 |
|---|---|---|---|
| G1 | 权限不变 | 升级包 `permissions` 块零变更（归一化文本哈希比对） | `SCL_004` |
| G2 | 测试不变 | 升级包不含 `tests/**` 任何路径变更 | `SCL_005` |
| G3 | deny 与门控不变 | deny 5 项完整；`self-scale.ps1` 哈希未变 | `SCL_004` |
| G4 | 职能块守恒 | 升级后职能块总数 = 18 且逐部门分布 = 6/2/3/3/4 | `SCL_010` |
| G5 | 别名完整 | 所有旧 slug 有别名映射，无一对多冲突 | `SCL_003` |
| G6 | 验收通过 | 机器可查子集（file_count=29、frontmatter 三元组、四处版本一致、5 个 D2、前缀清单、enum=auto+5、03-prompt 存在且 agent-invoked≥L3）；完整 §15 验收为人工步骤 | `SCL_006` |

G1–G3 不可绕过（即使人工批准）。升级包**排除** `__pycache__`/`*.pyc`。

### 12.4 slug 别名机制（向后兼容）

升级后旧 slug 全部保留为别名（写入 `scaling.md` 的 Alias Map 与 frontmatter `department_aliases` 指针）。micro→small：`governance-and-delivery` → {`governance-and-operations`, `quality-and-delivery`}；`engineering-and-safety` → {`technology-and-platform`, `security-and-compliance`, `people-and-growth`}（一对多）。

### 12.5 降级策略（禁自动）

降级有损（错误码需重映射、职能块数变化），**必须人工批准**，不自动执行（P38）；`self-scale.ps1` 无降级通道，降级按人工流程，`SCL_008` 语义由外部安装器承载。只允许降一档。

### 12.6 `.scaling-state.json`（全档位必备）

```json
{
  "schema_version": 1,
  "current_tier": "micro",
  "tier_history": [],
  "next_evaluation": "<ISO8601，默认 +30 天>",
  "last_metrics": { "agent_count": 0, "routing_accuracy": 0.0, "max_blocks_per_department": 0, "error_code_reuse_ratio": 0.0 },
  "pending_proposals": []
}
```

约束：`current_tier` 与 frontmatter `scale_tier` 一致（P41）；`tier_history` **只追加**不得改删（审计）；`validation.gates_passed` 必须 = 6；`validation.file_count` 用本档期望值（micro 25 / small 29）；初次生成时 `tier_history` 与 `pending_proposals` 为空。

---

## 13. 测试（`tests/test-method-patterns.py`，四类断言）

- **A 行为测试**：10 模板各 ≥1 条（正常+边界）。模板代码在 method-patterns.md 的 ```` ```python ```` 块内——用正则提取第 3 节代码块 `exec` 到独立命名空间后调用（**测源文件，非内联副本**）。`mask_sensitive_data` 必须断言 email/IP/phone 三类均脱敏。
- **B 源文件完整性**：`test_templates_source_exists`（权威源存在 + 10 个 def）、`test_phone_masking_in_source`（`[PHONE]` 在源中）、`test_legacy_templates_file_absent`（templates.md 不存在）。
- **C 结构一致性**：`test_function_block_conservation`（micro=18）、`test_scaling_files_present`（四件套 + propose-only）、`test_governance_files_present`（13 文件含 AGENTS.md）、`test_no_filename_with_space`、`test_prompt_modes_declared`（01/02 为 human-paste）、`test_human_paste_prompts_self_contained`（H1/H2/H6）、`test_language_policy_declared`、`test_skill_md_is_index_only`（正文 ≤120 行、无 def、无具体错误码）。
- **D 不可变边界**：`test_upgrade_package_excludes_immutable`（扫描 `{WORKSPACE_ROOT}/.skill-upgrade/`，不含 tests/ 与 permissions 变更；目录不存在时 skip）。

工程要求：`unittest` 风格，`python tests/test-method-patterns.py` 直跑；`SKILL_DIR` 用 `Path(__file__).resolve().parent.parent` 相对推导（禁硬编码）；时间用 `datetime.now(timezone.utc)`（禁已弃用 `utcnow`）；仅标准库；UTF-8 无 BOM。

---

## 14. 红线清单（P1–P55，完整内联；本包唯一权威）

> 本节是本包所有 `P##` 引用的**本地定义处**。生成或修改任何文件前，先核对相关行。

### 14.1 结构与命名

| # | 禁止 | 理由 |
|---|---|---|
| P1 | 部门子目录放 `SKILL.md` | 被加载器误注册为独立技能，triggers 冲突 |
| P2 | 子清单 `dependencies.skills` 填包内部门名/legacy 名 | 依赖解析失败；与根 `dependencies: []` 矛盾 |
| P3 | 各部门用不同章节骨架 | 无法程序化解析（源包 11 部门 5 种变体） |
| P4 | 写下与实际不符的数量宣称 | AI 照错误数字找文件，找不到即幻觉补全 |
| P5 | 章节编号跳号 | Agent 被迫下沉 D3，违背渐进式披露 |
| P6 | 合并档位丢失被合并职能的职能块 | 用职能块守恒(=18)自检 |
| P7 | 把 D4 引擎列为部门 | 与 department 枚举不符 |
| P8 | 留下孤儿文件 | 无文档引用即不可达 |
| P9 | 同一模块留两份命名相近文件 | 连字符版无法 import |
| P10 | 共享代码存两份 | 无法判断权威源（权威源见 P44） |
| P27 | 部门 slug 不符 §10.4 规范 | 产出不一致命名 |
| P28 | 破坏 §10.1 合并树严格包含关系 | 升级路径无法机械推导 |
| P29 | 重排既有 WFT 编号 / 用 001–099 放扩展 | 核心集编号固定，扩展走 WFT-1xx |
| P33 | 合并档位只写部门级章节、省略职能块 | 等于丢掉被合并部门职能 |
| P40 | 职能块标题用自由格式 | 无法程序化统计（须 `## FB-<N>: <ROLE>`） |

### 14.2 版本与元数据

| # | 禁止 | 理由 |
|---|---|---|
| P11 | 版本号多处各写各的 | 源包 5 处 2 值 |
| P12 | Changelog 同版本号出现两次或日期倒挂 | 审计混乱 |
| P13 | 路线图宣称的版本在 Changelog 无条目 | 虚假承诺 |
| P14 | 错误码编号留空洞 | 无法判断废弃还是漏写 |
| P15 | `name` 用 YAML 块标量(`\|`/`>`) | 转义风险；用单行引号 |
| P16 | `description` 超 1024 字符 | SkillImport 硬校验失败 |
| P17 | 错误码全表内联 frontmatter | D1 层超标，每次加载全量吞入 |
| P30 | L/G 档 department 枚举内联 frontmatter | 击穿行预算（微型档内联 3 项合法） |
| P31 | `scale_tier`/`department_count`/`function_block_count` 缺失或矛盾 | 档位须留痕且自洽 |
| P41 | `.scaling-state.json` `current_tier` 与 frontmatter 不一致 | 升级起点无法判断 |
| P42 | major 版本号与档位序号不对应 | 破坏升级可追溯性 |

### 14.3 安全

| # | 禁止 | 理由 |
|---|---|---|
| P18 | 硬编码绝对用户路径 | 换机必然失败 |
| P19 | 引用不存在的脚本/文件路径 | 断链 |
| P20 | 写任何真实或"示例"密钥 | 只写环境变量名 |
| P21 | 扩大 `permissions.files.write` 到 `{SKILL_DIR}` | 技能目录必须只读；升级不构成放宽理由 |
| P22 | 删减 `permissions.files.deny` 任何一项 | P0 级安全边界 |
| P23 | 回滚逻辑先删后恢复 | Copy 失败即永久丢失整包 |
| P24 | 安全门/Harness 文档写未实现的内容 | 虚假安全承诺 |
| P25 | 使用 `Invoke-Expression`/`iex`/`DownloadString` | 恶意行为首要特征 |
| P26 | 平台适配只做一半 | 非 Windows 下失效 |
| P32 | 契约声明与代码实现不一致 | 如 mask 契约要 [PHONE] 而代码缺 |
| P34 | 升级包含 `tests/**` 变更 | 自我豁免漏洞 |
| P35 | 升级包含 permissions/deny/门控变更 | 自我提权漏洞；人工批准也不放行 |
| P36 | 技能自行安装升级包（写 `{SKILL_DIR}`） | 违反 P21；只能 propose-only |
| P37 | 升级时未生成 slug 别名映射 | 破坏向后兼容 |
| P38 | 自动执行降级 | 降级有损，须人工批准 |
| P39 | 产物未通过自己文档写的验收脚本 | 生成后必须跑自定义验收 |

### 14.4 内容规格（对应本文各章）

| # | 禁止 | 对应 |
|---|---|---|
| P43 | `SKILL.md` 正文超 120 行或含代码/完整错误码表/SOP | §6.2 |
| P44 | 生成 `references/templates.md` 或任何文件内联复制模板 | §7.3 |
| P45 | prompt 未声明 mode，或 01/02 标为 agent-invoked | §11.1 |
| P46 | human-paste prompt 引用内部路径/标识符或缺填空位 | §11.2 |
| P47 | 源文件写死输出语言（如 `All content in English`） | §6.3 |
| P48 | 翻译六类不可变标识符 | §6.3 |
| P49 | Harness < L3 交付，或声明级别高于可查证据 | §8.2 |
| P50 | 按档位裁剪治理与社区文件 | §3（13 个全档齐备） |
| P51 | 错误文件名（`.gitingnore`/`changelog.md`/`CODE OF CONDUCT.md`）或含空格文件名 | §3 |
| P52 | 主模块超 300 行 / 子模块反向链接 / 一子目录被两主模块指向 | 集群化 |
| P53 | 为通用文件创建空文件或占位内容 | §4 Step 10 |
| P54 | 实现阶段治理文件未按文件树顺序生成 | §4 Step 10 |
| P55 | `AGENTS.md` 复述 `SKILL.md` 内容、成为第二入口，或缺首屏职责声明/超 150 行 | §6.2 / AGENTS.md |

### 14.5 工程卫生

不提交 `__pycache__`/`.pyc`；不缺 `.gitignore` 或用精确名而非通配（P39）；不提交安装器产物/本地审核报告(`REVIEW-*.md`)/`.skill-upgrade/` 提案包；**不 ignore `.scaling-state.json`**（它是包元数据）；不让测试自包含副本而不校验真实源文件；不让 README 的 Project Structure 与磁盘不符；代码块不用裸围栏；源文件不用非 UTF-8 或带 BOM。

---

## 15. 验收清单（每次生成/修改后必须执行）

```powershell
# 1. 测试套件（24 条应全绿，1 skip 属预期）
python tests/test-method-patterns.py

# 2. 升级就绪检查（只读）
powershell -File scripts/self-scale.ps1 -Action evaluate
```

**计数与一致性抽查**：文件总数 **25**；治理文件 **13/13**；职能块 **8+10=18**；错误码 **34**（CEO 12 + CTO 12 + SCL 10，编号无空洞）；frontmatter ≤85 行；SKILL 正文 ≤120 行；AGENTS.md ≤150 行；triggers 15 条。

**逐字符/一致性**：`permissions` 与 §9.1 逐字符一致；版本号四处同值（1.0.0）；许可四处同值（GPL-3.0）；D2 各 FB `### 4` 与 error-codes.md 同码同文；README 三兄弟结构树与磁盘 25 文件逐项一致；README.en.md 与 README.md 内容一致；无 BOM；无硬编码路径（`grep -rn 'C:\\Users\|c:/Users'` 零命中）；无 `templates.md`；每个 `def <fn>` 恰 1 处；无 `__pycache__` 残留。

## 16. 修改协议与已记录事项

**修改协议**：① 改前读 `AGENTS.md` 与本文 §5；② 结构性修改（增删文件/部门/FB/错误码）必须同步 README 三兄弟结构树、SKILL.md 索引、error-codes.md、`_meta.json` 版本、CHANGELOG；③ **不可触碰** `permissions` 块、`tests/` 期望值、`self-scale.ps1` 门控逻辑——即使人工批准也不得通过升级通道变更（§9.5）；④ 改完跑 §15 全部验收（P39）。

**已记录事项**：

| 项 | 说明 |
|---|---|
| 文件数 25 | 本文（`README-FOR-AI.md`）是独立项目的组成部分，非偏离项 |
| Core Identity 无「所属域」 | 微型档无域概念（域路由 L+ 档启用） |
| 记忆/熔断/董事会阶梯 | D2 中以 "at M+/L+ tiers" 限定语承载（微型档不引入这些子系统） |
| G6 为机器可查子集 | `self-scale.ps1` 的 G6 实现可自动化子集，完整 §15 验收为人工步骤（已如实声明，非 P24） |
| 更高档位 | M/L/G 的部门全集遵循 §10.1 同一合并树原则；本包当前只实现 micro→small 升级边 |

---

*本文为 `ai-company` 独立项目的唯一权威生成规格，GPL-3.0，完全自包含。修改本文本身也须遵守 §16 协议。*
