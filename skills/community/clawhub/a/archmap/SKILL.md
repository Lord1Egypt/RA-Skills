---
name: archmap
description: 架构测绘 Agent。零参调用自动分流（无基线→full 全量初始化，有基线→lite 极简增量），full/lite 显式词强制兜底；项目路径+需求文本做增量影响面分析；+sync 同步变更并重生成全套报告；+diff 产出行级差异影响面与测试选择（diff_impact.json）并留痕变更历史（时间+修改内容，复盘前固定卡点）。实现精准开发、节约tokens。
aliases: ["/archmap"]
---

# ArchMap 架构测绘 Agent

终端原生 Agent，无 Web 界面。零参调用自动分流 full/lite，另支持增量需求影响面分析、sync 同步、diff 影响面等显式模式。

## 身份定位（2026-08-15 用户裁定）

archmap = **纯分析方**：只做架构测绘与影响面分析、产出分析文档（`full_index.json` / `diff_impact.json` / `diff_history.jsonl` / 01~09 号报告等），不执行、不校验、不评分。消费侧是否按 `diff_impact.json` 圈定范围、如何校验执行结果，属于消费方（如 `whitebox-coverage`）自己的责任域与评分域——**消费侧扣的分归消费侧，不属于 archmap**；archmap 不为任何消费侧的合规性背书。

### 评估依据备注（2026-08-16 用户裁定，供后续评估直接援引，无需执行）

1. **零记录两种解释**：`diff_history.jsonl` 为 0 记录时必须先分流——「工作期本无代码变更」属正常零记录（机制设计使然：无变更不产出台账），**不等于机制空转**；只有「有变更但未执行 diff」才是失效。判据分流已机械化（gate-switch `archmap_diff_freshness` 闸的无变更豁免）。评估时拿零记录当空转证据 = 归因错误（2026-08-15 二评 archmap 90→86 误评即此，已勘误）。
2. **粒度弱不是缺陷**：模块拆分只到 api/方法（函数）级是用户有意设计（见「模块粒度设计裁定」），评估时不得按「拆分不够细」扣分。
3. **消费侧问题不归 archmap**：消费方不读 diff_impact、凭 git status 圈范围等问题，扣消费方的分，archmap 只对分析产物的正确性负责。

## 安装与依赖

首次使用前在本技能根目录执行 `pip3 install -r requirements.txt`（详见 `README.md`）。其中 sentence-transformers 为可选依赖，缺失时向量识别自动回退本地哈希向量化，功能可用、精度略降。

## 触发方式

```
/archmap <项目路径>                        # 零参自动分流（推荐）
/archmap <项目路径> full | lite [备注]      # 强制模式兜底
/archmap <项目路径> <需求文本>
/archmap <项目路径> sync
/archmap <项目路径> diff [修改内容备注]
```

示例：

```
/archmap /Users/xujin/projects/my-app
/archmap /Users/xujin/projects/my-app 新增用户积分系统，涉及登录接口和角色表
/archmap /Users/xujin/projects/my-app sync
```

## 模式路由（零参自动分流，2026-08-12 新增）

零参调用 `/archmap <项目路径>` 按基线存在与否全自动分流，无人工切换开关：

- **无基线**（`archmap/full_index.json` 不存在）→ 自动执行 full 完整初始化
- **有基线** → 自动执行 lite 极简增量（日常迭代默认，见模式 G）
- 特殊场景手动兜底：`full` / `lite` 显式词强制指定（大重构后 `full` 重生成完整图谱，无需删基线目录）

## 模式清单

### 模式 A：全量分析（只输入项目路径）

路径是项目根目录时：

1. 执行全量源码扫描
2. 按业务目录拆分模块，多线程 Worker 解析
3. 母体聚合资产、标记共享 API/存储、生成向量缓存
4. 生成 Mermaid 文本图表与 01~09 号 Markdown 报告
5. 结果原子写入 `<项目路径>/archmap/`
6. 输出产物路径和摘要

产物路径：

```
<项目路径>/archmap/
├── full_index.json          # 完整架构基线
├── vector_cache.json        # 模块向量缓存
├── 01_执行摘要.md
├── 02_架构图.md              # Mermaid 文本
├── 03_数据链路图.md
├── 04_时序图.md
├── 05_模块资产清单.md
├── 06_API资产清单.md
├── 07_存储资产清单.md
├── 08_依赖矩阵.md
└── 09_粒度校验报告.md
```

### 模块粒度设计裁定（2026-08-15 用户裁定）

模块拆分粒度上限 = **api 与方法（函数）级**，禁止拆得更细。理由：越精细扫描成本越大；粒度以「消费方能据此找到：模块↔方法映射、功能↔文件位置」为够用标准，核心目的是**省 token**。

### 模式 B：增量影响面分析（项目路径 + 需求文本）

输入已有基线对应的项目路径，并附加需求文本。本模式会在匹配需求前先同步源码中的实际变更，因此**调用 `/archmap <路径> <需求>` 即触发复盘整合**：

1. 读取 `<项目路径>/archmap/` 下的 `vector_cache.json`、`full_index.json`、`module_hashes.json`
2. 对比当前源码与上次同步时的模块内容指纹（SHA256），识别已变更/新增的模块
3. **仅重新解析变更模块并合并回基线**，未变更模块直接复用基线数据
4. 将需求文本向量化，与**最新模块向量**做余弦相似度匹配
5. 区分高置信/低置信疑似模块，递归遍历上下游依赖
6. 仅对需求命中的新增/修改模块启动 Worker 解析，存量依赖模块直接复用基线数据，不调用 LLM
7. 对命中的模块做**模块内精准定位**：识别涉及文件、函数/类名、接口路由、路由→文件映射，并按需求关键词相关度排序
8. **召回补强（recall_engine）**：向量命中基础上，用两类确定性信号扩展受影响集合，不受向量阈值约束——① 路由供需闭包（受影响模块引用的路由→定义方模块，及其定义路由的引用方模块）② 需求路由关键词硬匹配（需求词含 CN→EN 扩展，直接命中模块 defined 路由）。输出 `match_sources` 标注每个模块的命中来源（vector/keyword/route_closure/route_keyword）
9. 合并更新基线，生成 `precise_analysis.json` 影响面文件 + `precise_meta.json` 预测元数据（需求文本、命中来源、基线哈希指纹）
10. 输出受影响的模块、API、存储、涉及文件清单，指导精准开发

> 说明：复盘同步只在“已有基线 + 新需求”时触发；首次全量分析新项目不会执行同步。

产物：基线文件夹内更新 `full_index.json`、`vector_cache.json`，并新增 `precise_analysis.json`：

```json
[
  {
    "module_id": "src_users",
    "module_path": "src/users/",
    "files": [
      {
        "file_path": "api.py",
        "functions": ["list_users", "get_user"],
        "classes": [],
        "routes": ["/api/users", "/api/users/<id>"],
        "relevance": 0.6
      }
    ],
    "route_to_files": {
      "/api/users": ["api.py"],
      "/api/users/<id>": ["api.py"]
    },
    "keyword_matches": ["api.py"]
  }
]
```

### 模式 C：同步更新（项目路径 + sync）

在项目已完成全量分析并进入持续开发后，新增代码需要被合并回已有基线，而不是重新执行全量分析。

触发：

```
/archmap <项目路径> sync
/archmap <项目路径> 同步
```

执行流程：

1. 读取 `<项目路径>/archmap/` 下的 `full_index.json`、`vector_cache.json`、`module_hashes.json`
2. 对比当前源码与上次同步时的模块内容指纹（SHA256）
3. 仅重新解析**新增/修改**的模块，已解析过的未变更模块直接复用基线数据，不调用 LLM
4. 从基线中移除已删除的模块及其向量
5. 重新生成 Mermaid 图表与 01~09 号 Markdown 报告
6. 原子更新 `full_index.json`、`vector_cache.json`、`module_hashes.json` 与报告文件
7. **召回验证（recall_engine）**：若基线内存在上次影响面分析的预测文件（`precise_analysis.json` + `precise_meta.json`），自动比对预测模块与本次实际变更模块：
   - 有变更 → 产出 `recall_report.json`（命中率、漏报模块及归因：route_keyword_miss / closure_miss / vector_miss），追加 `recall_history.jsonl`，随后消费预测文件
   - 无变更 → 保留预测，待开发完成后下次同步再验证
   - 基线哈希指纹不一致（预测属于已结束的旧开发周期）→ 丢弃陈旧预测，不验证

产物：基线文件夹内容全量刷新，结构与模式 A 一致，但只消耗变更模块的解析成本。存在待验证预测时新增 `recall_report.json` 与 `recall_history.jsonl`。

```
<项目路径>/archmap/
├── full_index.json          # 已合并新增/修改模块
├── vector_cache.json        # 仅变更模块向量重新计算
├── module_hashes.json       # 最新模块内容指纹
├── 01_执行摘要.md
├── 02_架构图.md
├── 03_数据链路图.md
├── 04_时序图.md
├── 05_模块资产清单.md
├── 06_API资产清单.md
├── 07_存储资产清单.md
├── 08_依赖矩阵.md
└── 09_粒度校验报告.md
```

典型使用节奏：

1. 首次：`/archmap /path/to/project`
2. 开发新功能并修改源码
3. 复盘同步：`/archmap /path/to/project sync`
4. 定位影响：`/archmap /path/to/project 新增积分功能`

### 模式 D：ETL 底层规则探查（自动触发）

对含 ETL 特征目录的项目（`tongue_diagnosis/etl` / `etl_config` / `etl/core` 任一存在），全量分析与同步更新时**自动生成 7 项 ETL 变更维护服务产出**，写入 `<项目路径>/archmap/etl_rules/`：

| # | 产出 | 内容 |
|---|------|------|
| ① | `ETL规则索引总目录.md` | 7 分层目录树（预处理清洗→Chunk分片→向量化写入→一致性对账→隔离存储→异常重试→ETL编排）+ 规则唯一编码（ETL-CHUNK-01 等）+ 关键词标签 + 检索快捷索引 + 7 步使用流程 |
| ② | `details/ETL-{编码}.md`（每规则 1 份） | 统一 7 章节：规则基础标识 / 完整底层执行逻辑 / 源码精准定位 / 输入输出约束 / 关联依赖规则 / 历史改动记录 / 测试校验标准 |
| ③ | `etl_rule_mapping.json` | ETL规则-代码-配置映射对照表（机器可读） |
| ④ | `ETL规则依赖链路图.md` | Mermaid 依赖图 + 文字影响清单 + 影响分级（高/中/低） |
| ⑤ | `ETL全局参数基线表.md` | 全部规则参数基线值 + 配置文件来源 |
| ⑥ | `ETL规则变更风险评估清单.md` | 全部规则风险等级/描述/回归测试 + 变更前置动作 |
| ⑦ | `etl_rule_search_index.json` | 机器检索索引（规则条目 + 关键词快捷索引 keyword → 规则编码） |
| ⑧ | `ETL配置契约对齐报告.md` + `config_contract_report.json` | 配置-代码契约漂移检测（定期对齐）：yaml 键实存 + read/use 特征串 grep → aligned（已接线）/ unused（死配置）/ stale（代码残留）/ missing_from_yaml（契约不一致）+ 处置建议 |

要点：
- **定期对齐（配置契约漂移）**：改配置/改代码消费点后跑 `/archmap <项目路径> sync`，⑧报告自动刷新每字段状态（字段存在 ≠ 生效：unused/stale 需按处置建议接线或清理）；已有基线漂移示例：RRF 权重未生效（`rag_engine._rrf_fuse` weights 写死 1.0）、`max_ctx_tokens` 配置未接线、`reconcile.enabled/batch_size` 死配置、`embedding.yaml batch_size` 未消费
- 源码定位行号**运行时按函数名/特征串 grep 解析**，改代码后 `/archmap <项目路径> sync` 即刷新全部行号与产出
- **P0/P1/P2 解析深度分级（2026-08-12 二期）**：risk_level 高→P0 深度解析（行号+配置+契约）、中→P1 标准解析（行号）、低→P2 轻量解析（仅文件存在性校验，行号跳解析且不计入 unresolved 口径）；详情文档头部/索引总目录/mapping JSON/search_index JSON 均携带 priority 标识，summary 含 priority_counts 与 parse_depth 统计；单条规则可在 `etl_rule_registry.py` 显式写 `priority` 字段覆盖推导
- **回填约定（修改 ETL 规则/步骤/配置后必须执行）**：`/archmap <项目路径> sync` 自动回填三方面——① 行号（grep 实时解析）；② 参数基线（`etl.yaml`/`embedding.yaml`/`chunking.yaml` 运行时读取，③⑤⑦ 中对应规则参数自动刷新为配置文件当前值）；③ 语义级变更（规则改名/行为变更/风险等级调整）在 `etl_rule_registry.py` 追加 `history` 记录后重跑 sync 重生成。不执行 sync 则文档与代码/配置漂移。**回填完成判定禁止手写（2026-08-16 裁定，gate-switch 机械门禁）：声称"sync 已回填"前必须扳 `python3 ~/.agents/skills/gate-switch/scripts/gate_switch.py --spec ~/.agents/skills/gate-switch/specs/archmap_sync_freshness.json --set project=<项目路径> --set etl_config=<被改 ETL 配置路径>` 照抄结论——判 A（`archmap/etl_rules/ETL配置契约对齐报告.md` 新于被改配置）才允许声称；判 B = 先跑 sync 后重扳。**
- 检索入口：读 `etl_rules/etl_rule_search_index.json`（机器）或索引总目录关键词表（人工）
- 详情文档含测试校验标准章节，改完规则按对应用例回归
- 自定义 ETL 规则注册表覆盖机制见 README.md「项目级配置」一节

## 模式 E：测试设计输入资产（Test Design Input Assets）

ArchMap 全量分析产出的架构图、数据链路图、时序图、资产清单、依赖矩阵，可直接作为 `test-case-designer` 的输入，驱动「节点 + 分支 + 方法」三要素测试设计。

### 可被测试设计消费的产物

| 产物文件 | 测试设计用途 | 提取内容 |
|----------|--------------|----------|
| `02_架构图.md` | 识别系统分层与模块边界 | 分层节点（Trigger/Definition/Persistence/Engine/Validation） |
| `03_数据链路图.md` | 识别端到端数据流 | 数据流节点、输入输出、持久化落点 |
| `04_时序图.md` | 识别调用顺序与并发/等待关系 | 调用时序、同步/异步边界、异常返回点 |
| `05_模块资产清单.md` | 识别功能模块与职责 | 模块名、核心函数、职责描述 |
| `06_API资产清单.md` | 识别接口测试节点 | 路由、方法、参数、返回结构、错误码 |
| `07_存储资产清单.md` | 识别数据持久化测试点 | 存储类型、字段、约束、生命周期 |
| `08_依赖矩阵.md` | 识别变更影响面与回归范围 | 模块间调用关系、共享 API/存储 |
| `precise_analysis.json` | 增量需求时精准定位测试范围 | 变更模块、涉及文件、函数/路由、相关度 |

### 测试设计输入标准格式

`test-case-designer` 读取上述产物后，必须将信息归约为以下标准结构（作为设计中间产物随 `execution-list.json` 一并提交审核，**不作为 archmap 产物文件落地**——archmap 引擎产物仅 01~09）：

```markdown
## 测试节点清单（Node Inventory）

| 节点编号 | 节点名称 | 所在模块 | 功能/作用 | 输入 | 输出 | 持久化 |
|----------|----------|----------|-----------|------|------|--------|
| N-001 | create_workflow_endpoint | webui.py | 通过 Web UI 创建新工作流 | {name, mode} | flow.yml / SKILL.md / 目录 | 新建目录树 |
| N-002 | validate_flow_structure | workflow.py | 校验 flow.yml 结构合法性 | flow_data | 错误列表或空列表 | 无 |
| N-003 | gate_a_check | engine.py | 执行前准入校验 | agent, state | passed/errors/log | engine_state.json |

## 分支闭环清单（Branch Closure）

| 源节点 | 分支条件 | 真分支 | 假分支 | 非法输入 | 状态不一致 |
|--------|----------|--------|--------|----------|------------|
| N-001 | name 是否为空 | 继续创建 | 返回 400 | 超长/特殊字符 | 父目录未设置 |
| N-003 | upstream 是否全部完成 | 进入 Gate B | blocked | 未知节点 | 交付物哈希被篡改 |

## 测试方法映射（Method Mapping）

| 节点 | 边界值(BV) | 等价类(EC) | 需求逻辑(DL) | 场景(SC) | 异常(EX) | 兼容(CP) | 接口安全(IS) |
|------|------------|------------|--------------|----------|----------|----------|--------------|
| N-001 | 名称长度边界 | 有效/无效名称 | 创建→生成→返回 | 正常创建流程 | 父目录缺失 | — | 路径穿越/特殊字符 |
| N-003 | max_retry 边界 | 上游完成/未完成 | Gate A→执行→Gate B | 正常推进 | 哈希不匹配 | 有/无 jsonschema | — |
```

### 增量场景下的消费方式

当 PM 给出新增需求时：
1. 调用 `/archmap <项目路径> "需求文本"` 生成/更新 `precise_analysis.json`。
2. `test-case-designer` 优先读取 `precise_analysis.json` 中的变更模块与涉及文件。
3. 仅对变更模块及其直接依赖模块提取测试节点，避免全量重设计。
4. 在 `execution-list.json` 中标记 `baseline_affected: true` 的用例，用于精准回归。

### 与 test-case-designer 的对接契约

`test-case-designer` 具备自主分析能力，启动后按以下逻辑处理：

1. **自主发现现有分析结果：** 检查 `<项目路径>/archmap/` 是否存在且包含有效的 `02_架构图.md` 与 `03_数据链路图.md`。
   - **若存在：** 直接读取 `02~08` 号产物 + `precise_analysis.json`（增量场景），作为测试设计输入，避免重复分析。
   - **若不存在或已过期：** 自行调用 `/archmap <项目路径>`（全量）或 `/archmap <项目路径> "需求文本"`（增量）生成分析结果，再读取使用。**PM 无需在测试前单独调用 archmap。**
2. 读取 `02_架构图.md` + `03_数据链路图.md` + `04_时序图.md`，识别系统级测试节点。
3. 读取 `05_模块资产清单.md` + `06_API资产清单.md` + `07_存储资产清单.md`，识别模块级测试节点。
4. 读取 `08_依赖矩阵.md`，识别节点间依赖与影响面。
5. 输出归约后的节点/分支/方法清单作为设计中间产物（即规则 32 Step 1.8《测试节点与分支清单》），随 `execution-list.json` 一并提交审核。

### 模式 F：diff 影响面分析（项目路径 + diff，2026-08-12 新增）

版本更新后的差异化影响面分析，为白盒增量测试等下游提供权威 diff 输入。**git 无关**（无仓库项目可用），零 LLM 调用，秒级完成。

**执行时机（固定卡点）：功能新增/修改完成后、复盘阶段前必须执行一次。** 本次变更（时间+修改内容+行区间+影响闭包）自动记入变更历史，作为复盘的输入材料；验收通过后再用 sync 刷新基线并回补 01~09 分析文档——diff 记录、变更历史、分析文档三者构成一个整体。

触发：

```
/archmap <项目路径> diff
/archmap <项目路径> diff 本次给视频变速功能增加非法参数校验
```

执行流程：

1. 读取基线目录行级快照 `file_line_hashes.json`（full/sync 时自动写入；首次 diff 无快照则初始化并提示下轮起可比对）
2. 逐文件 difflib 比对当前行哈希与快照 → 输出变更文件的精确变更行区间（1-based，合并相邻区间）。**未变更文件仅做哈希比对，不做任何重新分析**
3. 依赖图（含根目录文件，不依赖模块扫描粒度）三类边：Python import（AST）、JS/TS/Vue import/require（正则+别名解析）、跨语言路由供需边（路由定义×字面量引用，双向）；缓存走 `file_imports.json` + `file_routes.json`，仅变更/缓存缺失文件重新解析；新增或删除文件属结构性变更，全量重解析一次防边缺失。v2 起快照覆盖 `.py/.ts/.tsx/.js/.jsx/.vue/.sql/.yaml/.yml`，v1 快照自动迁移
4. 从变更业务文件出发沿反向导入边 BFS → 影响闭包（变更文件 + 全部传递依赖方）；测试文件仅作汇点不传播
5. 测试选择：选中 = 闭包内测试文件 ∪ 自身变更的测试文件；标记 `untested_changes`（闭包内无任何测试的变更业务文件）
6. 若项目根存在 `coverage-tiers.json`，按最长前缀匹配为每个变更文件标注 tier
7. 产出 `<项目路径>/archmap/diff_impact.json`；**行级快照不在 diff 模式更新**（保证同一工作期重复比对结果稳定），随下次 full/sync 刷新
8. **有变更时自动留痕**：追加 `diff_history.jsonl`（机器可读，含备注与变更指纹 `fingerprint`）并重渲染 `10_变更历史.md`（时间+修改内容+变更文件区间+闭包+测试选择）；零变更运行不记录。**幂等去重**：追加前与台账末条指纹（changed_files+changed_ranges+symbols 的 sha1 前 12 位）比对，同指纹（同一变更区间重复跑 diff）跳过写入并提示「幂等跳过：同指纹变更已记录（#N）」，台账不刷重复记录；指纹字段缺失的旧记录视为不同指纹，向后兼容

产物结构：

```json
{
  "changed_files": [{"path": "ui/main_window.py", "change_type": "modified", "tier": "P2", "changed_ranges": [[169, 182]]}],
  "deleted_files": [],
  "affected_closure": {"files": ["..."], "changed": ["..."], "propagated": ["..."]},
  "test_selection": {"selected": ["tests/test_main_window.py"], "skipped": ["..."], "untested_changes": []},
  "stats": {"changed_files": 1, "changed_ranges": 1, "closure_files": 3, "tests_selected": 1, "tests_skipped": 7},
  "history_path": "<项目路径>/archmap/diff_history.jsonl",
  "history_doc": "<项目路径>/archmap/10_变更历史.md"
}
```

下游消费：`whitebox-coverage` 增量模式以 `diff_impact.json` 为唯一范围依据（选择性执行 + `--diff-scope` 缺口过滤 + diff_gate 门禁）；复盘流程以 `10_变更历史.md` 为变更台账输入。

### 模式 G：lite 极简增量（零参调用且有基线时自动进入，或显式 `lite`，2026-08-12 新增）

日常开发迭代的默认模式。与 sync 的差异：**不重生成 01~09 全量报告与架构大图**，只做变更闭环，秒级完成：

1. 行级快照比对检测变更（与模式 F 同一引擎，git 无关）
2. 仅重解析变更模块并合并回基线（full_index / vector_cache / module_hashes / 行级快照 / 导入图缓存全部刷新）
3. 有变更自动留痕：追加 `diff_history.jsonl` + 重渲染 `10_变更历史.md`（可带修改内容备注）
4. ETL 项目自动刷新 `etl_rules/` 产物；存在未验证预测时照常做召回验证
5. 产出/刷新 `diff_impact.json`（含 `direct_dependents` 一级依赖摘要 + 全量传递闭包，机器读全闭包不占 Agent 上下文）

零变更时直接返回「无变更，无需更新」。01~09 报告需要反映最新代码时跑 `sync` 或 `full`。

## 底层调用

包装脚本位置：

```bash
/Users/xujin/.agents/skills/archmap/archmap <项目路径> [需求文本]
```

等价于：

```bash
# 全量
python3 /Users/xujin/.agents/skills/archmap/archmap /path/to/project

# 增量
python3 /Users/xujin/.agents/skills/archmap/archmap /path/to/project "新增用户积分系统"
```

引擎包 `archmap_agent` 已随技能自包含分发（与包装脚本同目录），无需另外安装引擎。

## 专家槽位（SLOT-1 建议槽 / SLOT-2 内化槽，2026-08-15 接入）

遵循 `/Users/xujin/.agents/skills/expert-router/docs/slots-protocol.md` 协议。核心理念：**自己做的是自己的，别人教的也是自己的**。

### SLOT-1 · 专家建议槽（挂载点：解析触发参数后、调用引擎前）

1. 组装路由文本：`{模式名} {需求文本或项目特征}`，如 `增量影响面分析 新增用户积分系统，涉及登录接口和角色表`
2. 调 expert-router 挑专家小组（archmap 任务聚焦，Top-4~8 即可）：

   ```bash
   python3 /Users/xujin/.agents/skills/expert-router/scripts/route.py "<路由文本>" --top 6
   ```

3. 对每张建议卡逐条裁决：`accepted`（说明怎么落实：转化为校验点 / 报告关注点 / 分析维度）｜`rejected`（说明理由）｜`deferred`（说明触发条件）。**禁止静默忽略**
4. 裁决结果 append 落盘 `<项目路径>/archmap/expert_advice.jsonl`（含时间、模式、建议卡、裁决、理由）
5. accepted 的建议必须在交付摘要中回链 expert_id（如"按 A04-E05 建议，本次测绘额外标注了共享存储边界"）

模式与优先领域参考（路由结果不佳时手动指定方向）：

| 模式 | 优先领域 |
|---|---|
| full / lite 测绘 | A04 系统架构、F05 系统设计思维 |
| 增量影响面（需求文本） | F05 系统设计思维、A04 系统架构、A05 数据库与存储 |
| diff 影响面 | B02 自动化测试、A08 性能优化 |
| sync 同步 | A06 DevOps与部署 |

**豁免**：零变更的 lite（返回"无变更，无需更新"）跳过 SLOT-1——无事可建议时不走形式。

### SLOT-2 · 技能内化槽（挂载点：产物交付后、任务收尾前）

对每条 accepted 建议强制执行**复盘三问**（v1.1：沉淀的是**通用方法**，不是任务总结）：

| # | 问题 | 要求 |
|---|---|---|
| Q1 | 我为什么没想到？ | 盲区归因：知识缺口 / 思维惯性 / 上下文缺失 / 工具不熟 |
| Q2 | 这条建议背后是什么方法？ | 抽象到 L2 通用方法：方法名 + 它解决的**问题族**（一类相似问题的通用特征，禁止出现本项目具体名词） |
| Q3 | 我缺什么技能才能自己提出它？ | 写成 L2 技能卡：触发条件 + 思考路径 + 操作要点；洞察到深层思维习惯（L3 元技能）单独标注 |

产出 append 落盘 `<项目路径>/archmap/internalizations.jsonl`，字段以协议 v1.1 为准（`skill_name` / `problem_family` / `method_core` / `thinking_path` / `verify`）。

**入库闸门（按产出内容定轨：领域技能广而大 / 专项技能窄而深）**：
- 先尝试抽象成领域技能过三道闸：① 抽掉本项目名词方法依然成立？② 换同类问题能直接指导行动？③ 技能名是动词性"方法"不是名词性"事情"？
- 抽象不上去但**会复发 + 有具体操作深度**（步骤/参数/坑位）→ 落专项技能（允许含场景名）
- 只满足其一 → 不入库，记任务日志；同类专项攒 ≥3 张时回顾一次，能合并抽象就晋升领域技能

示例对照（L0 禁止，L1/L2 按产出定）：
- ❌ L0 任务记录："这次给积分系统标了共享存储边界"
- ✅ 专项技能（窄而深）："`archmap-diff-vue-alias-debug`——diff 模式下 Vue 别名解析失败的排查套路：场景族=archmap diff + Vue 项目；含具体坑位与解析顺序"
- ✅ 领域技能（广而大）："`boundary-explicitization`——分析任何系统时，先把隐式共享的资源/状态/接口揪出来显式标注；问题族=一切需要看清系统结构边界的分析任务"

内化铁律：

1. **不归因不收尾**：存在 accepted 建议而 `internalizations.jsonl` 无过闸记录，任务不得标记完成。回链落盘判定禁止手写，必须扳 `python3 ~/.agents/skills/gate-switch/scripts/gate_switch.py --spec ~/.agents/skills/gate-switch/specs/slot_attribution.json --set project=<> --set expert_id=<>` 照抄输出（落实质量留软层）
2. **下次先查自己**：同模式任务启动 SLOT-1 之前，先按 `problem_family` 检索 `internalizations.jsonl`，命中则直接自用——同一类问题不重复问专家
3. **分道执行**：命中的领域技能融入当前分析（作为检查维度，点到即止）；命中的专项技能**升格为执行主线**——按卡内步骤/参数/坑位逐项深入核查，每项留执行痕迹，浅尝辄止视同未触发
4. **向下催生（选择性，不强迫）**：领域技能首次在新场景族执行后，评估是否有"不写下来下次会忘"的场景级细节——有才产出配套专项技能（`parent_skill` 挂到方案名下），没有则留一行"无需细则"评估备注即可；单次任务最多催生 1 个，禁止凑数
5. **晋升通道**：成熟的技能卡可交 `retro-skill-dispatcher` GENERATE 模式注册进全局技能库，完成从"项目级经验"到"全局技能"的晋升

## 约束

- 不启动任何 Web 服务。
- 不读写 SQLite 任务表。
- 所有状态保存在项目路径下的 `archmap/` 文件夹内。
- 不修改用户原始业务代码，仅做静态源码分析。
- 全量模式只扫描业务目录，自动过滤 test、node_modules、dist、build 等目录。
- 增量模式复用存量基线资产，不重复解析未变更模块，显著降低 Token 消耗。
- 输出均为 JSON/YAML/Markdown/Mermaid 纯文本，不生成图片。
