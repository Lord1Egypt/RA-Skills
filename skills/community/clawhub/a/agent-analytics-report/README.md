# agent-analytics-report

> 生成 Agent 用量分析报告：Token 消耗趋势、缓存命中占比、各模型成本对比、异常自动预警。支持日 / 周 / 月 / 年。
> **数据源可切换：WorkBuddy（默认）+ Claude Code + Codex CLI + 千问办公。**

---

> **文件角色**：本技能 = 1 个声明（SKILL.md）+ 5 个数据源适配器（`adapters/`）+ 核心引擎（`scripts/`）。`tests/` 与 `tools/` 是开发期资产（测试 / CI 渲染），不在用户运行路径上、也不进发布包；`docs/` 与 `examples/` 是文档与示例，不含可执行逻辑。

## 当前支持范围

| 数据源 | `--source` | 状态 | 读取位置 |
|---|---|---|---|
| WorkBuddy | `workbuddy`（默认） | ✅ | `~/.workbuddy/`（traces + `workbuddy.db` + `usage-log.json` + 会话目录） |
| Claude Code | `claude-code` | ✅ | `~/.claude/projects/**/*.jsonl` |
| OpenAI Codex CLI | `codex` | ✅ | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` |
| 千问办公 QwenWork | `qwenwork` | ✅（⚠️ token 为本地估算，**不可对账**） | `~/.qwenworkcn/projects/**/*.jsonl` + `logs/runs/` + `agents.db` |
| 百度搭子 DuMate | `dumate` | ⚠️ 通用入口（数据归属未证实） | `~/.workbuddy/`（按 WorkBuddy 布局读取），支持 `DUMATE_HOME` / `DUMATE_OUTPUTS_DIR` 覆盖 |
| Trae 等 | — | ⬜ 未实现 | — |

**对账源**（叠加在 WorkBuddy 之上，把成本从估算升级为真值）：

| 对账源 | 参数 | 状态 | 读取位置 |
|---|---|---|---|
| 官方用量导出 | `--import-official <xlsx>` | ✅ v1.6.0 | 官网下载的 `request-usage-*.xlsx`（纯本地只读解析） |

- **WorkBuddy**：完整能力，含技能调用、自动化运行、任务分类；
- **Claude Code**：解析会话日志的 token / 成本 / 任务类型 / 每日趋势，无技能与自动化维度（JSONL 里没有这两类数据）。
- **千问办公**：调用次数、请求耗时、模型档位、会话真名、**技能调用**、**交付物**、**定时任务**
  都是**真实值**（技能取自转录里的 `Skill` 工具调用、交付物取 `present_files` ∪ `outputs/` 目录、
  定时任务取 `agents.db` 的 `task_run_logs`）；但服务端**不回传 token**，token 由本地字符估算，
  且积分订阅无公开单 token 价 → 报告自动进入 **`tokens_only` 计价模式**（撤掉所有 ¥ 金额，
  金额、花费速览、省钱杠杆等章节整章缺席，补价后自动恢复）。
  ⚠️ **千问办公服务端不回传 token，报告中的 token 为字符估算；估算值不可用于对账或账单核对**，真实消耗请以千问办公官方账单为准。详见
  [ADAPTERS.md](docs/ADAPTERS.md) §四、§4.6。
- **百度搭子 DuMate**：`--source dumate` 是**读取 WorkBuddy 布局目录的通用
  入口**——任何把数据写进 `~/.workbuddy/` 布局的第三方客户端都能用它采集
  （token、成本、技能调用、自动化运行、会话、产出文件、记忆日志，维度同
  WorkBuddy）；报告标题显示「百度搭子使用情况报告」，并支持 `DUMATE_HOME`
  （覆盖数据目录）、`DUMATE_OUTPUTS_DIR`（单独覆盖产出 / 记忆目录）两个环境变量
  （多账号 / 未来布局变更的隔离点）。
  ⚠️**数据归属未证实，请勿当作「百度搭子用量」引用**：实测
  `workbuddy.db` 217 个会话里百度搭子相关命中 0 行、1165 个 trace 无任何归属
  字段（跑出的 16 会话 / 161 trace 100% 是 WorkBuddy 的），该客户端自有数据在
  `~/.qianfan/` 下且为 yml 流转格式、不在本技能 trace schema 内。
  详见 [ADAPTERS.md](docs/ADAPTERS.md) §6.1 / **§6.4（归因红线）**。
- **官方用量导出**：本地 trace 的成本是**估算**（静态价表无法表达服务端时段减免，且漏记图像模型 / minimax-m3 约 8.7%）。
  导入官方导出后成本取「积分」字段，升为 **L1 真值**，报告新增 §3.5 双源对账。详见
  [ADAPTERS.md](docs/ADAPTERS.md) §二 / §五。
- 计价库 `scripts/pricing.json` 内含 **WorkBuddy 官方接口的模型与单价**（非通用市价，含 GLM-5.3 / GLM-5.3-Flash / Hy4 preview 等），以及 Claude 系列模型的**人民币折算估算价**（以 Anthropic 美元刊例价为准，可用 `pricing.local.json` 覆盖）；
- 升级机制依赖 `skillhub upgrade`。

新增数据源的扩展方式见 [ADAPTERS.md](docs/ADAPTERS.md)。
- 版本发布与更新日志见 [releases.md](docs/releases.md)（含各版本 GitHub Release 链路与速览）。

---

## 功能

- **Token 分析**：消耗趋势、原始 vs 实际（含缓存抵扣）、缓存占比
- **成本估算**：按模型公开单价计算，以实际账单为准；限免模型自动标注（如混元 Hy3 限时免费至 2026-10-31、Hy4 preview 至 2026-09-10，期间花费记 ¥0.00）
- **免费额度版 / 收费版合并显示**：同一模型的两个入口（如 `hy4-preview` 与 `hy4-preview-x`、`hy3` 与 `hy3-x`）在报告中合并为一行，费用只计收费版用量——合并只改显示分组，不碰计费（`pricing.json` 的 `display_merge` 段可增删合并对）
- **异常双口径**：成本 + Token 独立检测，免费期高流量也不漏报；脏数据显式警告
- **自定义模型（Bring Your Own Models）**：带上你自己的模型一起计费，升级不丢
- **报告格式**：Markdown / HTML（含交互图表、浅深色自适应）/ JSON

---

## 安装

### 方式一：SkillHub（推荐）
在 SkillHub 搜索 `agent-analytics-report` 一键安装。

### 方式二：手动
```bash
git clone <your-repo-url> ~/.workbuddy/skills/agent-analytics-report
```
重启 WorkBuddy 后技能生效。

### 在千问办公（QwenWork）里安装
千问办公按目录扫描技能，装到自己的技能目录即可（无需 `_meta.json`）：

```bash
# Windows（PowerShell / Git Bash 均可，注意展开 ~）
git clone <your-repo-url> ~/.qwenworkcn/skills/agent-analytics-report
# 或在 SkillHub 安装后，把技能目录拷到 ~/.qwenworkcn/skills/ 下
```

装好后在千问办公里直接说「生成我用量报告 / 周报」，或用命令行：

```bash
cd ~/.qwenworkcn/skills/agent-analytics-report
python scripts/collect_usage_data.py --source qwenwork --period week -o data.json
python scripts/generate_report.py data.json --output report.html --format html
```

> ⚠️ 记得带 `--source qwenwork`：默认源是 WorkBuddy，本机没有 `~/.workbuddy/` 时会采不到数据。

---

## 使用

```bash
# 1. 采集最近 7 天数据
python scripts/collect_usage_data.py --period week --output data.json

# 2. 生成报告（Markdown + HTML）
python scripts/generate_report.py data.json --output report.md   --format markdown
python scripts/generate_report.py data.json --output report.html --format html
```

### 切换数据源（Claude Code / Codex CLI / 千问办公）

```bash
# Claude Code
python scripts/collect_usage_data.py --source claude-code --period week --output data.json
# 自定义 Claude Code projects 目录
CLAUDE_PROJECTS_DIR=/path/to/projects \
  python scripts/collect_usage_data.py --source claude-code --period week --output data.json

# OpenAI Codex CLI
python scripts/collect_usage_data.py --source codex --period week --output data.json

# 千问办公（在千问办公里跑就用这个）
python scripts/collect_usage_data.py --source qwenwork --period week --output data.json
QWENWORK_HOME=/path/to/.qwenworkcn QWENWORK_DB=/path/to/agents.db \
  python scripts/collect_usage_data.py --source qwenwork --period week --output data.json

python scripts/generate_report.py data.json --output report.html --format html
```

### 计价模式（无单价的数据源）

```bash
# 默认 auto：本期一个单价都没命中时自动切 tokens_only（千问办公就是这种）
python scripts/collect_usage_data.py --source qwenwork --period week -o data.json
# 显式强制
python scripts/collect_usage_data.py --source qwenwork --cost-mode tokens-only -o data.json
python scripts/collect_usage_data.py --source qwenwork --cost-mode priced    -o data.json
```

`tokens_only` 下报告只讲用量：撤掉成本货币化、花费速览、省钱杠杆、最贵模型、档位与缓存可省测算，
模型表退化为「模型 / 调用次数 / 实际消耗Token」三列，§四 换成「Token 与调用深度分析」，
§3.1 表标题改为「Token 维度明细」，「缺失单价 + 补价 stub」整块也随之压制（金额都不算了，
再摆一张补价表属于误导）。priced 模式下若只是**部分**模型缺价，该块照常出现。
数据源若天生不支持计费（千问办公积分无法归因到会话），在适配器里声明
`SUPPORTS_COST = False`，该块连 priced 也不出现。

---

## 测试（pytest + Allure）

本技能附带一套分层回归测试，覆盖从数据采集、计费等效折算、报告生成到发布一致性的全链路。**全部用例使用合成 fixture 数据，不引用任何第三方商业 API、不含真实用量/个人信息**，可安全公开（适合作为作品集在 GitHub Pages 展示）。

测试分层（共 25 个测试文件、587 用例全绿）：

| 层 | 文件 | 覆盖要点 |
|----|------|----------|
| **L0 数据采集** | `test_cost_math.py` · `test_calendar_period.py` · `test_aggregation.py` · `test_display_merge.py` · `test_mode_rates.py` · `test_no_broad_except.py` · `test_example_report_sanity.py` | 计价（GLM 折扣 / 缓存折算 / 限免 / blended 回退）、日历周期对齐、聚合与异常双口径检测、display_merge 合并显示与计费分离、档位维度（快速/均衡/极致）倍率锚定与归一、禁止宽泛异常捕获、示例报告健康度 |
| **L1 报告生成** | `test_report_generation.py` | GLM-5.2 家族合并、XSS 转义、图表构建、三格式（md / html / json）跑通 |
| **L2 定价边界** | `test_pricing_boundary.py` | 通道分支、已下架模型、零/负/超大值、blended 精度 |
| **L3 CLI 端到端** | `test_e2e_cli.py` | 黑盒 subprocess 跑通报告生成三格式、CLI 参数校验、恶意模型名 XSS 回归 |
| **L4 发布一致性** | `test_publish_parity.py` | `config.json` / `metadata.json` 版本对齐、交付物齐全、`.gitignore` 闸门（敏感产物不进包） |
| **L0 适配器** | `test_claude_code_adapter.py` | Claude Code JSONL 解析、日期窗口过滤、缓存折扣与成本、坏行健壮性、会话派生与任务分类、`--source claude-code` CLI 黑盒（fixture 走 `CLAUDE_PROJECTS_DIR`，不读真实目录） |
| **L0 适配器** | `test_codex_adapter.py` | Codex CLI rollout JSONL 逐轮 `turn.completed` 解析、跨版本字段兼容（`type`/`item_type`、reasoning 字段）、缓存折扣、`--source codex` CLI 黑盒（`CODEX_HOME` 隔离） |
| **L0 适配器** | `test_qwenwork_adapter.py` | 千问办公三源归一（转录 / 逐次调用日志 / agents.db）：requestId 分组、字符估算与上下文累加、日志耗时关联、上游回传真值后自动升级、DB 增强与缺失降级、毫秒时间戳等坏数据健壮性、`--source qwenwork` CLI 黑盒与标题口径横幅（`QWENWORK_HOME` / `QWENWORK_DB` 隔离，不读真实目录） |
| **L0 计价模式** | `test_cost_mode.py` | `_decide_cost_mode` 三条边界（限免/本地合法 ¥0 不误判、L1 优先、显式开关覆盖）、tokens_only 下 MD/HTML 金额章节与表头缺席、历史 JSON 缺 `cost_mode` 按 priced 零回归、JSON 落盘 `meta.cost_mode`、页脚按数据源署名；第二批：调用粒度按源分流、真实提问轮数取代聚类估算、后台运行摘要行、`cost_hidden` 下的 Token 口径下期预测与峰值日承接、`single_channel` 跳过 §3.2、token 口径异常条目 📈/💰 分列、分母口径补充 —— **每条都配一条 WorkBuddy 侧「不许变」断言** |
| **L0 千问办公维度** | `test_qwenwork_dimensions.py` | 技能调用取自转录 `tool_use.Skill`（含窗口过滤、按调用次数计、按日期去重）、交付物 = `present_files` ∪ `outputs/` 磁盘扫描（跳过 `.bak`/`.tmp`/`~$`/隐藏、同路径不双计、文件缺失优雅降级）、`scheduled_tasks ⟕ task_run_logs` 五字段契约（`result_success` 不得缺，否则汇总 KeyError）、无 cron 的机器返回真 `[]`、`nudge_logs` 只出全局摘要不混入自动化 |
| **L0 官方导出** | `test_official_usage.py` | xlsx 纯标准库解析（明文/共享串/inlineStr/日期序列）、**按表头名映射（新版 6 列不取 Prompt 的回归门禁）**、缺列报错、聚合与免费判定、双源对账、`--import-official` CLI 端到端（USERPROFILE 隔离）、零回归、L1/L2 渲染与脏数据回落 |
| **L0 任务分类** | `test_task_classification.py` | 加权评分取代首匹配、词边界（fix≠prefix）、信号密度取胜、置信度、task_rules.json 外置与回退、LLM 分类器 mock 全路径、collect_task_types 独立可调用（v1.3.0 拆分漏导入回归） |
| **L0 定价更新** | `test_fetch_pricing.py` | 条目校验（schema/负数/倍率）、候选与 diff 产出、--apply 备份落盘、过期检查退出码、`FETCH_PRICING_ROOT` 隔离黑盒 |
| 既有 | `test_channel_attribution.py` · `test_session_labeling.py` | 通道归因、跨窗口会话补全、孤儿 trace 合并、任务类型标签正确性 |

运行方式：

```bash
cd agent-analytics-report

# 1. 安装测试依赖（建议隔离 venv）
python -m venv .venv && .venv/Scripts/python.exe -m pip install -r requirements-tests.txt

# 2. 运行全部测试并生成 Allure 原始数据
.venv/Scripts/python.exe -m pytest tests/ -v --alluredir=allure-results

# 3a. 用本机 Java 渲染原生交互报告（可选）
.venv/Scripts/python.exe -m allure serve allure-results

# 3b. 渲染自包含 HTML 仪表盘（无需 Java，适合 GitHub Pages 静态托管）
.venv/Scripts/python.exe tools/render_allure_html.py --results-dir allure-results --output allure-report.html
```

- 用例按 `tests/conftest.py` 的 marker 体系标注（`smoke` / `unit` / `integration` / `regression` / `golden` / `metadata` / `privacy` …），可用 `-m` 过滤，例如 `pytest -m regression`；
- 报告含用例步骤树、参数、归因明细附件；本机若装有 Java，也可直接 `allure serve allure-results` 消费同一份数据；
- 测试仅依赖标准库 + `pytest` + `allure-pytest`，**不引用任何第三方商业 API**；`allure-results/` 与 `allure-report*` 已被 `.gitignore` 排除，不进发布包。

---

## 自定义模型（BYOM）

发布版只内置 **WorkBuddy 官方在用模型 + 官方已下架历史模型**，`custom_local` 段为空 `{}`。

你自己的第三方 / 自建模型（OpenRouter 免费、硅基流动、自建 Ollama 等）写在**本机** `scripts/pricing.local.json`——
该文件已被 `.gitignore` 排除，**不进发布包，`skillhub upgrade` 升级也不会覆盖**，单价自动保留。

当你显式发起「自定义模型注入」流程时（说一句"把我的自定义模型加进报告"），Agent 才扫描本机用过的 `custom-local:*` 模型及 `~/.workbuddy/models.json` 中配置的自定义 / 外部 / Ollama 端点（扫描按需触发、非报告默认流程），**逐个问你单价；只有你明确给出单价数字、
并确认过待写入条目清单之后**，才写入本地文件。之后用自然语言告诉 Agent 新增模型即可。

> **授权边界**：上述扫描**仅限 `~/.workbuddy` 这一个目录**，写入**仅限 `scripts/pricing.local.json` 这一个文件**。
> **生成报告本身不触发这两个动作**——报告的默认流程是只读采集 + 只写报告产物。
> 你也可以只要清单、先不写入（明说「先只列出来给我看，不要写文件」即可）；拿不到单价的模型会标「待补」跳过。
> 详见 [`references/on-download-inject.md`](references/on-download-inject.md) 与 [`references/add-custom-models.md`](references/add-custom-models.md)。

---

## 常见问题

花费对不上、模型显示「未配置」、想加自己的模型、想知道那些小图标什么意思——集中解答见 [references/FAQ.md](references/FAQ.md)（36 问，单篇自足）。

---

## 架构与扩展

| 文件 | 职责 |
|------|------|
| `scripts/collect_usage_data.py` | 数据采集门面（当前为 WorkBuddy 适配器）；内部已拆分为 `ca_core` / `ca_sources` / `ca_sessions` / `ca_aggregate` 四模块，门面仅做 `from X import *` |
| `scripts/generate_report.py` | 报告渲染（四色标记：🔀路由 / 🏠本地 / 🔧外部自定义 / 🗄️官方已下架） |
| `scripts/pricing.json` | 官方模型计价库（含 `delisted` 历史下架模型、`display_merge` 显示合并配置） |
| `scripts/pricing.local.json` | 用户本地覆盖（gitignore，不发布） |
| `references/` `examples/` | 操作手册与使用示例 |

多 Agent 扩展方式见 [ADAPTERS.md](docs/ADAPTERS.md)。

---

## License

MIT © Elisabeth15501 2026
