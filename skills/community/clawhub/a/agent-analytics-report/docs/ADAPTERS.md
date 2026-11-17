# 多 Agent 数据源适配（ADAPTERS）

本技能通过 `--source` 参数切换**数据源适配器**。适配器负责把某个 Agent 的原生用量记录
归一化为统一 schema，下游的聚合、计价、报告渲染逻辑**完全复用**。

| 数据源 | `--source` 值 | 状态 | 数据位置 |
|---|---|---|---|
| WorkBuddy | `workbuddy`（默认） | ✅ 内置 | `~/.workbuddy/` |
| Claude Code | `claude-code` | ✅ 已实现 | `~/.claude/projects/**/*.jsonl` |
| OpenAI Codex CLI | `codex` | ✅ 已实现（MVP，需真实样例复核） | `~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl` |
| 千问办公 QwenWork | `qwenwork` | ✅ 已实现（⚠️ token 为本地估算，见 §四） | `~/.qwenworkcn/projects/**/*.jsonl` + `logs/runs/` + `agents.db` |
| 百度搭子 DuMate | `dumate` | ✅ 已实现（复用 WorkBuddy 布局，见 §六） | `~/.workbuddy/`（可用 `DUMATE_HOME` 覆盖） |
| Trae 等 | — | ⬜ 未实现 | 见文末「新增一个 Agent」 |
| OpenClaw | — | ⬜ 未实现（规划中） | 见文末「新增一个 Agent」 |

**对账源**（与 `--source` 正交，仅 `workbuddy` 可用，用于把成本从估算升级为真值）：

| 对账源 | 参数 | 状态 | 数据位置 |
|---|---|---|---|
| 官方用量导出 | `--import-official <xlsx>` | ✅ 已实现（v1.6.0） | 官网下载的 `request-usage-*.xlsx` |

> ⚠️ 在适配器实现并验证前，请勿在文档 / 市场文案中声称已支持该 Agent。
> Codex 适配器已通过单元测试（11 例，覆盖解析 / 日期过滤 / 缓存折扣 / 健壮性 / CLI 端到端），
> 但由于 Codex CLI rollout schema 跨版本有差异（如 `reasoning_output_tokens` vs `reasoning_tokens`、
> `type` vs `item_type`），建议用一份你本机真实 `rollout-*.jsonl` 跑一次 `--source codex` 复核后再对外宣称支持。
> 千问办公适配器：23 例单元测试 + **本机真实数据端到端**（7 日窗口 154 次调用 / 16 个会话）均已跑通，
> 但它是目前**唯一连 token 都需要本地估算**的数据源（服务端不回传用量），能力边界见 §四。

---

## 一、快速使用

```bash
# Claude Code 数据源（自动定位 ~/.claude/projects）
python scripts/collect_usage_data.py --source claude-code --period week -o data.json
python scripts/generate_report.py data.json --output report.html --format html

# 自定义 projects 根目录（非默认安装位置 / 测试）
CLAUDE_PROJECTS_DIR=/path/to/projects \
  python scripts/collect_usage_data.py --source claude-code --period week -o data.json

# 千问办公数据源（自动定位 ~/.qwenworkcn 与 %APPDATA%/QwenWorkCN/data/agents.db）
python scripts/collect_usage_data.py --source qwenwork --period week -o data.json
python scripts/generate_report.py data.json --output report.html --format html

# 自定义千问办公主目录 / 业务库（多账号、非默认安装位、测试）
QWENWORK_HOME=/path/to/.qwenworkcn QWENWORK_DB=/path/to/agents.db \
  python scripts/collect_usage_data.py --source qwenwork --period week -o data.json
```

`--source` 与 `--period` / `--days` / `--start` / `--end` 可自由组合，周期语义不变。

```bash
# 官方用量导出（成本真值 L1）——叠加在 workbuddy 源之上
python scripts/collect_usage_data.py --start 2026-09-12 --end 2026-09-14 \
  --import-official ~/Downloads/request-usage-2026-09-13.xlsx -o data.json
python scripts/generate_report.py data.json --output report.html --format html
```

---

## 二、官方用量导出适配器（`--import-official`）

实现文件：`adapters/official_usage.py`（v1.6.0 / F17）

### 2.1 为什么需要它

本地 trace 只有「generation 粒度」的模型调用，存在两类**静态价表在数学上无法弥补**的偏差：

| 偏差 | 表现 | 实测（30 日窗口） |
|---|---|---|
| **盲区** | 图像模型、minimax-m3 等根本不进 trace | 漏记 **¥251.74**（占 WorkBuddy 成本 8.7%） |
| **标签不分免费/收费** | `hy4-preview` 夜间免费、白天收费，trace 的 `model` 字段两者相同 | 12 次调用里 11 次实际 0 积分，静态价表全计成收费 |
| 粒度差 | 官方 1「请求」 ≈ trace 11.9「generation」 | 802 请求 vs 9222 generation |

官方导出的「积分消耗」是**服务端实际计费结果**，是唯一真值。

### 2.2 导出格式与解析规则（实测两版）

| 版本 | 列顺序 |
|---|---|
| 旧版（~2026-09-12） | RequestID / 积分消耗 / 模型 / 客户端 / 时间 |
| 新版（2026-09-13 起） | RequestID / 积分消耗 / **User Prompt** / 模型 / 客户端 / 时间 |

- 所有单元格均为**明文字符串**（含积分与时间），无共享字符串、无日期序列值。
- 图像模型「客户端」列为空；聚合时归入 `(空)`。
- 时间为**北京时间**；trace 是 UTC，对账前已归一（`ca_core.TZ = UTC+8`），不存在 ±8h 错位。

> ⚠️ **禁止按固定列位解析**。官方 09-13 加列后，按列位解析会把 `User Prompt` 当成模型名
> （已在调试脚本里踩过一次）。适配器一律**按表头名映射**（大小写 / 空格不敏感，中英文别名均可），
> 缺任一必需列（模型 / 积分 / 时间）直接报错，不做猜测。

解析用标准库 `zipfile` + `xml.etree` 直接读 xlsx（zip + XML），**不引入 openpyxl**，
保证技能在任意用户机器上零依赖可用。同时兼容共享字符串（`t="s"`）、`inlineStr` 与日期序列值。

### 2.3 产出结构

`collect_official_usage(path, start_date, end_date)` 返回：

```python
{
  "source": "workbuddy-official",
  "rows":      [{request_id, credits, model, client, ts, date, hour, is_free, prompt}],
  "by_model":  [{name, requests, credits, free_requests, paid_requests, avg_credits}],
  "by_client": [...], "by_day": [...],
  "totals":    {requests, credits, free_requests, paid_requests, models, clients},
  "meta":      {file, sheet, columns, window, parsed_rows, skipped_rows},
  "filter":    {start_date, end_date},
}
```

`credits <= 0` 判为**免费请求**（官方对时段减免 / 免费额度的实际结果）。

`reconcile_with_trace(official, model_stats, alias_map=DISPLAY_MERGE)` 产出对账结果，
报告渲染为 **§3.5 双源对账**：`missing_in_trace`（官方有 / trace 无 → 成本被低估）、
`trace_only`（本地 / 免费 / 路由，不是漏记）、`both`（给粒度倍数）。

#### 2.3.1 变体归拢（`collapse_display_aliases`，v1.6.1）

trace 侧早已按 `display_merge` 把收费版变体归并显示为基名（`hy3-x` → `hy3`、
`hy4-preview-x` → `hy4-preview`，见 `ca_core.merge_display_key`）。**官方侧必须过同一层映射**，
否则精确匹配会对不上，把变体误报成盲区。

实测（30 日 / 802 请求）：不归拢时 `hy3-x`(97 / 397.43) 与 `hy4-preview-x`(1 / 13.52) 被误报，
虚报 410.95 积分 = `missing_credits` 的 75.7%；真实盲区只有 131.62。归拢后
`missing_credits` **542.57 → 131.62**，被归并的变体写进 `variants`，报告显示为 `hy3（含 hy3-x）`。

> ⚠️ **不做模型名归一化（v1.6.1 明确边界）**：这里只做 `display_merge` 里**显式配置**的
> 「同模型收费版变体」归拢，**不剥离 `custom-local:` 之类的来源前缀**。该前缀是
> 「WorkBuddy 自建 vs 外部 API」的唯一可辨识标识，剥掉就无法判断 token 归属；
> 来源信息另由 `is_local` / `is_custom` 通道标记承载，报告 §3.2 据此拆成
> 官方/网关 · 本地模型(🏠) · 外部 API(🔧) 三节。

### 2.4 成本两级制

| 级别 | 触发 | 成本来源 | 报告顶部横幅 |
|---|---|---|---|
| **L1 真值** | 传 `--import-official` | 官方「积分」字段 | ✅ 显示官方请求数 / 积分 / 免费次数 |
| **L2 估算** | 未传（默认） | 静态 `pricing.json` × token | ⚠️ 警告「不含时段减免，请勿据此对账」 |

`meta.cost_source` 标记本期口径。渲染层以「**是否真拿到官方数据**」为准而非标记本身——
标记是 official 但数据缺失时回落 L2，避免渲染出「L1 真值（未导入）」这种自相矛盾的横幅。

### 2.5 约束

- **纯只读**：只打开用户自己下载的本地文件，不写、不传、不联网（符合 ADR-4 / ADR-6）
- 仅 `--source workbuddy` 可用（其它 Agent 没有官方积分账单可对），混用退出码 2
- 导出按报告窗口过滤；窗口外的行数记入 `meta.official_import.rows_out_of_window` 并在 stderr 提示
- **零回归**：不传 `--import-official` 时，输出与 v1.5.x 完全一致（无 `official_usage` / `reconciliation` 键）

---

## 三、Claude Code 适配器

实现文件：`adapters/claude_code.py`

### 3.1 数据定位

`resolve_claude_projects_root()` 按以下优先级定位 projects 根目录：

1. `CLAUDE_PROJECTS_DIR` —— 直接指向 `projects/` 目录（测试与自定义安装位）
2. `CLAUDE_CONFIG_DIR` —— Claude Code 官方配置根覆盖，可逗号分隔多个根，取第一个含 `projects/` 者
3. 平台默认
   - Windows：`%APPDATA%/Claude/projects`
   - macOS / Linux：`~/.claude/projects`

`_iter_jsonl_files()` 递归扫描该目录下所有 `*.jsonl`，并兼容 Claude Desktop agent 模式的
`local-agent-mode-sessions` 嵌套 `projects/` 子树。

### 3.2 解析规则

会话文件（`<sessionId>.jsonl`）逐行 JSON，按 `type` 处理：

| 行类型 | 处理 |
|---|---|
| `user` | 记录 `cwd`；首条文本作为会话 `title`（截断 60 字符）；文本并入 `_dialogue_text` 供任务分类 |
| `assistant` | **有 `message.usage` 才产一条 trace**；无 usage 的行（纯思考 / 工具回显）跳过不计费 |
| 其它（`system` 等） | 忽略 |

字段映射（`assistant.message.usage` → 统一 trace）：

```
input_tokens                    → input_tokens
output_tokens                   → output_tokens
cache_read_input_tokens         → cached_tokens（计入缓存折扣）
cache_creation_input_tokens     → _cache_creation_input_tokens（透明字段，便于后续精细计价）
input + cache_read + cache_create + output → total_tokens
```

其余派生字段：`channel = "claude-code"`、`raw_model / model_key = "claude-code:<裸模型名>"`、
`effective_tokens` / `effective_cost` 走与 WorkBuddy 一致的缓存折扣口径（缓存命中只按 10% 计入）。

健壮性：坏 JSON 行、非 dict 行、缺字段行一律跳过（不抛异常）；会话元数据 `created_at` /
`updated_at` 取文件内最小 / 最大时间戳。

### 3.3 会话派生

Claude Code 没有独立的会话表，适配器从 JSONL 现场合成会话记录，字段与 WorkBuddy
`workbuddy.db → sessions` 对齐，使下游任务分类、Top 任务、会话榜无需改动：

```python
{
  "id": <文件名 stem>, "cwd": ..., "title": <首条 user 文本 60 字截断>,
  "custom_title": "", "status": "completed",
  "created_at": <最小时间戳 ms>, "created_date": "YYYY-MM-DD",
  "updated_at": <最大时间戳 ms>,
  "mode": "claude-code", "model": "claude-code:<首个 assistant 模型>",
  "is_background_automation": False, "version": "unknown",
  "_dialogue_text": "<全部 user/assistant 文本拼接>",   # 任务分类输入
}
```

### 3.4 计价

Claude 系列模型已写入 `scripts/pricing.json`（单位：元 / 百万 tokens）。**刊例价为美元，
本表按 ~7.2 折算人民币，仅为估算值**——请以 Anthropic 官方最新定价为准，或用
`scripts/pricing.local.json` 覆盖：

| 模型 | 输入 | 输出 |
|---|---|---|
| `claude-opus-4` / `claude-opus-4-5-20251101` | 108.0 | 540.0 |
| `claude-sonnet-4` / `claude-sonnet-4-20250514` | 21.6 | 108.0 |
| `claude-haiku-4` / `claude-haiku-4-20250514` | 5.76 | 28.8 |

`parse_channel()` 已识别 `claude-code:` 前缀，`price_of()` 对该通道取裸模型名单价。
未命中单价的模型走通用的「未配置」流程（计入 token、不计成本，并在报告中提示）。

### 3.5 已知限制（MVP）

- 只统计**单次对话内**的 token 与成本；Claude Code 不落盘会话级「任务名」，Top 任务榜以会话首条提问为题
- `duration_ms` 恒为 0（JSONL 无可靠的端到端耗时字段，未做推测）
- 不区分 Max 订阅 / API 计费：一律按刊例 API 价估算，订阅用户实际边际成本更低
- 子 Agent（Task tool）若写入同目录 JSONL 则已包含，否则不计

---

## 四、千问办公（QwenWork）适配器

实现文件：`adapters/qwenwork.py`

千问办公的会话内核是 qoder-agent-sdk（与 Claude Code 同构），转录格式相近，
但**用量口径完全不同**——它同时读三个本机数据源，各有分工：

| 数据源 | 位置 | 贡献的字段 | 性质 |
|---|---|---|---|
| 会话转录 | `~/.qwenworkcn/projects/<slug>/<sessionId>.jsonl` | 对话内容、cwd、时间戳、档位、`requestTokenAnchor.requestId` | 真实 |
| 运行日志 | `~/.qwenworkcn/logs/runs/<run>/qodercli.log` | **逐次模型调用**（`model.request.started` / `model.response.completed`）、端到端耗时、`stop_reason` | 真实 |
| 业务库 | `%APPDATA%/QwenWorkCN/data/agents.db`（只读） | 界面会话真名、`model_level` 档位、每轮 `durationMs` / `numTurns` | 真实 |

三者的连接键是 `requestId`：转录里一次响应被拆成 `thinking` / `text` / `tool_use` 多行，
它们共享同一个 `requestTokenAnchor.requestId`，归并后 = 日志里的一条
`model.response.completed` = **1 条 trace**（本机实测：一份 102 次调用的会话，
转录里的 requestId 与 `qodercli.log` 的 `request_id` 100% 对得上，无孤儿）。

### 4.1 ⚠️ 与 WorkBuddy 源的根本差异：token 也是估算

千问办公**服务端不回传 token 用量**。本机实测：`qodercli.log` 里 1167 条
`model.response.completed` 的 `input_tokens` / `output_tokens` /
`cache_read_input_tokens` / `cache_creation_input_tokens` **全部为 0**；
转录里 `message.usage` 恒为 `null`；`agents.db` 全文检索不到 token / usage / credit 字段。

| | WorkBuddy / Claude Code / Codex | 千问办公 |
|---|---|---|
| token | 上游回传**真值** | **本地字符估算** |
| 成本 | 静态价表 × token（L2 估算） | 无公开单 token 价 → **不计价**，报告自动切 `tokens_only`（见 §4.3） |
| L1 真值通道 | `--import-official` 官方积分导出 | **没有**：积分按账号计费，无法归因到单个会话 |

所以千问办公报告顶部有两道横幅：`token 口径：本地字符估算` +
`计价模式：tokens_only（仅用量，不计价）`，全篇不出现金额与花费结论。
**结构性结论（用了几次、什么时候、哪个会话、哪档位、耗时多久）可放心引用；
token 数字当趋势看，不要拿去对账。**

### 4.2 估算规则（`estimate_tokens`）

| 内容 | 规则 | 依据 |
|---|---|---|
| CJK 字符（中日韩 + 全角标点） | 1 字 ≈ 1 token | Qwen 系 BPE 实测 0.6~1.0，取 1.0 **偏高估** |
| 其余字符（拉丁 / 数字 / 符号 / JSON 结构） | 4 字符 ≈ 1 token | 业界经验 3.5~4.3 |
| 输入 token | 该请求**之前**全部已见内容的估算和 | 真实计费里 input ≈ 上下文重发 |
| 工具入参 / 回显 | 计入（`json.dumps` 后按同一规则折算） | 它们确实进过上下文，漏计会显著低估 |
| system prompt | **不计**（不落盘） | 实际 input 略高于估算 |

系数是模块常量 `CJK_TOKENS_PER_CHAR` / `LATIN_CHARS_PER_TOKEN`，便于复核与调参。
**不做缓存折扣**：`cached_tokens` 恒为 0，因此真去补价时成本会偏高（真实场景大量上下文命中缓存）。

### 4.3 计价与补价路径

trace 的 `model_key` 统一为 `qwenwork:<档位>`（`flash` / `pro` / `qwork-lite` /
`qmodel_latest`，取自服务端下发的标识符，不是裸模型名）。`ca_core.parse_channel()`
识别 `qwenwork:` 前缀，`price_of()` 剥前缀后按裸档位名查表——**发布版 `pricing.json`
故意不配这些档位**（没有公开单 token 刊例价，编一个数就是假数据），
于是按技能既有约定：计入 token、不计成本、报告提示未配置。

要看到金额，在 `scripts/pricing.local.json`（不进发布包）里按裸档位名补价：

```json
{
  "flash": {"input": 1.2, "output": 4.8},
  "pro":   {"input": 7.2, "output": 28.8}
}
```

**tokens_only 计价模式**（`--cost-mode`，跨数据源通用）：报告端不再摆着满屏
`¥0.00` 与「未配置」让人误读成「免费」或「采集失败」。

| 取值 | 行为 |
|---|---|
| `auto`（默认） | 本期**一个单价都没命中**时自动切 `tokens_only`。判定需同时满足：有未配置单价的模型 + 无任何已配置行 + 总额为 0 + 非 L1 真值 |
| `tokens-only` | 强制隐藏金额维度 |
| `priced` | 无论如何都按现状输出金额（历史行为） |

命中后 `meta.cost_mode="tokens_only"`，渲染层同步改口径：§一 成本行换成「计价状态」、
§2.2 成本货币化整节撤掉、§三 改名「模型使用对比」且模型表退化为用量三列、
§四 换成「Token 与调用深度分析」（每会话 Token Top10 / 分桶 / Token 异常）、
§3.4 档位维度与 §4.4 省钱杠杆 / §4.5 失败归因 / §4.6 缓存可省 / §十 花费速览全部缺席，
HTML 统计卡与表头同步撤掉金额列。§3.3「缺失单价模型 + pricing.local.json 补价 stub」整块
**在 tokens_only 下压制**，并且当适配器声明 `SUPPORTS_COST = False`（千问办公就是）时
**连 priced 模式也不给** —— 落 `cost_supported: false` 到 `meta`，报告端据此决定。
理由：千问办公的积分无法归因到单会话，那张补价 stub 引导用户填出来的金额是**永远无法对账的虚构值**；
真需要金额口径时用 `--cost-mode priced`，成本章节会回来，但 stub 不会误导。
priced + 该源支持计费 + 只是**部分**模型缺价时，该块照常输出 —— 那时它才真有用。

三条不误判的边界：限免 / 本地模型的 `¥0.00` 是**已配置单价**算出的真实结果（照常出金额）、
L1 官方账单在场时永远 `priced`、历史 JSON 缺 `cost_mode` 字段按 `priced` 渲染（零回归）。
判定逻辑抽成纯函数 `collect_usage_data._decide_cost_mode()`，边界由
`tests/test_cost_mode.py` 逐条钉住。

### 4.4 前向兼容：上游一旦回传 token 就自动转真值

`_parse_session_file` 对每条 trace 判定：日志里四个 token 字段**任一非 0** →
直接采用真值，并把 `_tokens_estimated` 置 `false`；全为 0 才走字符估算。
千问办公哪天在服务端补上 usage 回传，本适配器无需改代码即从「估算 token」升级为
「真值 token + 估算成本」，与 Claude Code / Codex 同口径（`test_real_usage_overrides_estimate` 守住这条路）。

### 4.5 已知限制

- **无 L1 真值**：账号级积分无法归因到单个会话，`--import-official` 对该源直接退出码 2
- `cached_tokens` 恒 0（无缓存命中数据），补价后成本会偏高
- `<synthetic>` 占位响应（中断 / 错误）不计为模型调用，只记入会话的 `_synthetic_responses`；
  千问办公的**记忆整理后台任务**（注入提问以 `Target file this round:` 开头）标
  `is_background_automation=True` 并改名「记忆整理后台任务（awareness nudge）」——
  它确实花额度，但不该出现在「Top 任务」榜里冒充用户任务
- 技能 / 交付物 / 自动化的侦测机制与 WorkBuddy 完全不同，见 **§4.6**（`memory_logs`
  该源确实无对应结构，恒空）
- 未做子 Agent 拆分：`isSidechain` 记录在 trace 的 `_is_sidechain` 透明字段里，但不单独归因
- 跨窗口长会话按 trace 日期计入窗口（与 claude-code / codex 同语义）
- 只读：全程 `mode=ro` 打开 SQLite、不写不联网（符合 ADR-4 / ADR-6）；DB 被进程锁住时自动降级为纯 JSONL 口径

### 4.6 技能 / 交付物 / 自动化的侦测机制（与 WorkBuddy 的根本差异）

WorkBuddy 这三件事各有**独立数据源**，千问办公全都不是那个形状。第一版适配器曾据此判
「该源无此维度」并把 §一/§七/§九 全部留空——**那是错的**：信号都在，只是要换个地方找。

| 维度 | WorkBuddy | 千问办公（权威源） | 归因粒度 |
|---|---|---|---|
| 技能调用 | `usage-log.json` 的 `firstSeenDate` / `recentDates[]` | 转录 `tool_use name="Skill"` → `input.skill` | 每次调用都有 `timestamp` + `sessionId`，**日期与会话双归因，比 WorkBuddy 更准** |
| 自动化运行 | `workbuddy.db` automation + runs | `agents.db` 的 `scheduled_tasks` ⟕ `task_run_logs` | `automation_id` / `auto_status` / `result_success` / `created_date` |
| 产出文件 | 扫 `~/WorkBuddy/` 会话目录 | `qwenwork_file_present_files` 的 `input.files[].file_path` ∪ 磁盘 `<cwd>/outputs/` | 前者有调用时刻（更准），后者只有 mtime |

配套约定：

- **`skill-usage.json` 不作统计源**：本机实测它只有 2 条累计记录，而转录里实到 17 次
  `Skill` 调用（低估约 8.5 倍），只当旁证；差异落 `meta.skill_usage_source` 说明取自转录。
- **`Write`/`Edit` 不混进交付清单**：只作为「改动过的文件」单独计数（本机 Edit 3305 次，
  混入会把 §九 淹掉）；磁盘兜底扫描跳过 `.bak` / `.tmp` / `~$` / 隐藏文件。
- **`nudge_logs` 不进 `automation_runs`**：本机 317 条后台运行里只有 26 条能 join 到会话
  （归因率约 8%），进 §八 会造出一堆 unknown 组；它只出全局摘要 `meta.background_runs`
  （次数 / 失败数 / 耗时 / 类型），§一 用一行交代，且 §十一 会据此提示失败率过高的空转。
- **定时任务显示 0 是真 0**：本机 `scheduled_tasks` 与 `task_run_logs` 均 0 行，此时
  报告写「本月无自动化任务运行记录」是对的——**不要**用「不适用」话术掩盖没采的事实。
- **`single_channel`**：千问办公只有一层通道（档位即入口），§3.2「按入口 / 通道模型」必然
  与 §3.1 同构，故采集端声明 `meta.single_channel=True`，渲染端跳过该节并留一行说明——
  同样走**显式声明**，不让渲染层靠「两表行数相等」隐式猜。

---

## 五、数据来源与已知偏差

> 本节回答一个问题：**报告里的数字，哪些能信、哪些只能看结构。**
> 数据来自 30 日官方导出 vs 本地 trace 的实测对标（2026-08-13 ~ 2026-09-12，WorkBuddy 客户端 773 条）。

### 4.1 两个数据源各自的口径

| | 官方用量导出 | 本地 trace |
|---|---|---|
| 粒度 | **请求**（一次用户提问 = 1） | **generation**（一次请求内可多轮生成） |
| 成本 | 服务端实际计费结果（`积分`） | 静态价表 × token **估算** |
| 时区 | 北京时间 | UTC（已归一 +08:00） |
| 覆盖 | 仅云端计费调用 | 含本地模型、免费额度、路由调用 |
| 可信度 | **L1 真值** | L2 估算（结构可信、金额不可信） |

同一份数据下，trace generation 数约为官方请求数的 **11.9 倍**——这是统计粒度不同，
**不是用量暴涨**。报告概览的「调用次数」已标注 `generation 粒度`。

### 4.2 trace 盲区（官方有、trace 无 → 成本被低估）

| 模型 | 性质 | 实测漏记 |
|---|---|---|
| `hunyuan-image-alpha` | 图像生成，客户端列为空 | ¥119.91 |
| `minimax-m3` | **WorkBuddy 客户端却不被 trace 记录** | ¥120.39 |
| `hunyuan-image-v3.0-art` | 图像生成 | ¥11.44 |
| **合计** | | **¥251.74（占 8.7%）** |

> 修正说明：早期版本曾把 `deepseek-v4-pro` 也列为盲区，实为 VSCode / Codebuddy 客户端调用，
> 不属于 WorkBuddy trace 的盲区，已剔除。

### 4.3 trace 独有（官方无 → 不是漏记，别去对账）

| 类型 | 例子 | 为什么不进官方账单 |
|---|---|---|
| 本地模型 | `custom-local:*` | 本机推理，零 API 成本 |
| 限免入口 | `hy3`（至 2026-10-31） | 官方侧免费，积分 = 0 |
| 路由别名 | `balanced-model` / `fast-model` | 未解析底层模型，P1 处理 |
| 免费时段 | `hy4-preview` 夜间 23:00–08:00 | 时段减免，积分 = 0 |

### 4.4 模型名不体现「是否免费」

同一个 `hy4-preview` 标签下，免费与收费的调用**模型名完全相同**：

| 时间 | 模型 | 时段 | 积分 |
|---|---|---|---|
| 2026-09-13 23:53 | `hy4-preview` | 夜间 | 0（免费） |
| 2026-09-12 11:32 | `hy4-preview` | 白天 | 43.40（收费） |
| 2026-08-29 02:42 | `hy4-preview-x` | 夜间 | 13.52（**`-x` 变体不参与夜间免费**） |

→ **绝不能靠模型名或调用时段推断是否免费**；免费状态只能从官方导出的「积分」字段读取。
→ `hy4-preview-x` 是「免费额度用尽后的收费变体」，`pricing.json` 维持 x0.29，**不得置 0**。

### 4.5 怎么办

1. **要准确金额** → 加 `--import-official <xlsx>`，报告切 L1 真值并出 §3.5 双源对账。
2. **只做趋势分析** → 默认 L2 即可，但别把金额当账单。
3. 受时段减免影响的模型已写入 `pricing.json` 的 `low_confidence` 段，L2 下标 ⚠ 并剔除出「最贵模型」结论。

---

## 六、百度搭子（DuMate）适配器

### 6.1 背景：当前按 WorkBuddy 布局读取该目录（数据归属未证实）

> ⚠️ **归因红线**：本适配器**不验证数据归属**。`--source dumate` 采集到的内容
> **可能完全是 WorkBuddy 的**，不可当作「百度搭子用量」对外引用。详见 §6.4。

百度搭子桌面客户端（qianfan-desktop-app / DuMate）当前的本地数据**按 WorkBuddy
的布局**落在 `~/.workbuddy`，本适配器因此按 WorkBuddy 那套路径常量读取：

| 数据 | 路径 |
|------|------|
| Traces（token / 模型 / 时长） | `<home>/traces/<pid>/trace_*.json` |
| 会话 / 自动化 / 信用 | `<home>/workbuddy.db` |
| 技能使用记录 | `<home>/usage-log.json` |
| 会话转录定位 | `<home>/projects/` + `sessions/` |
| 产出文件 / 记忆日志 | `$DUMATE_OUTPUTS_DIR` 或 `<home 同级>/WorkBuddy/<会话目录>` |

其中 `home` = `DUMATE_HOME`（默认 `~/.workbuddy`）。

**不要**把上表理解成「这些数据的归属已确认属于百度搭子」。目前这条链路上
**没有任何字段能区分数据来源**，所以本节的准确说法是「**当前按 WorkBuddy
布局读取该目录；数据归属未证实**」。

### 6.2 那适配器做什么

实现文件 `adapters/dumate.py`，三个职责：

1. **显式声明口径**：`--source dumate` 让报告标题 / 来源清单显示
   「百度搭子使用情况报告」，标明本次采集走的是这个入口，而不是借用
   WorkBuddy 的名义充当「另一份数据源」——它**不证明数据来自百度搭子**；
2. **路径隔离**：支持 `DUMATE_HOME` 覆盖数据目录（默认 `~/.workbuddy`），
   并可用 `DUMATE_OUTPUTS_DIR` 单独覆盖产出 / 记忆目录。若该客户端未来更换
   布局 / 迁移目录 / 多账号并存，只需在适配器内部重映射，不改采集器与报告端；
3. **可测试隔离**：测试通过 `DUMATE_HOME` 把 fixture 指向 `tmp_path`
   （`tests/test_dumate_adapter.py`），绝不读取用户真实目录。

技术要点：

- `collect_dumate` 复用 `ca_sources` 的采集链路（`collect_db_data` /
  `collect_traces` ×2 含跨窗口补全会话 / `collect_skill_usage` /
  `collect_session_outputs`），通过 `_patched_paths` 上下文**临时替换**
  `ca_sources` 模块级路径常量、用完恢复，改动面最小，不触碰 workbuddy 默认分支；
- `SUPPORTS_COST = True`：token 为上游回传真值（读的是 WorkBuddy 的 traces，
  非本地估算），成本可走静态价表估算（L2），`--import-official` 对账同样可用。
  该声明只关于**计价能力**，与数据归属无关；
- schema 与 WorkBuddy 一致，下游聚合 / 报表 / 任务分类零改动。

> 本适配器读作「WorkBuddy 布局目录」的**通用入口**，归属由使用者自行确认。
> 它**不是**「已验证支持百度搭子」的能力承诺。

### 6.3 使用

```bash
# 走 dumate 入口采集（报告标题显示「百度搭子使用情况报告」；
# ⚠️ 数据归属未证实，见 §6.4）
python scripts/collect_usage_data.py --source dumate --period week -o data.json

# DUMATE_HOME 覆盖数据目录（多账号 / 迁移场景）
DUMATE_HOME=/path/to/custom-home python scripts/collect_usage_data.py --source dumate --period week -o data.json

# DUMATE_OUTPUTS_DIR 单独覆盖产出 / 记忆目录（与 DUMATE_HOME 解耦）
DUMATE_OUTPUTS_DIR=/path/to/outputs python scripts/collect_usage_data.py --source dumate --period week -o data.json

# 生成报告
python scripts/generate_report.py data.json --output report.html --format html
```

### 6.4 ⚠️ 已知边界：数据归属未证实

这一条是**发版红线**，优先于本节其余内容。

**我们无法证明 `--source dumate` 采到的是百度搭子的数据。** 已做的排查：

| 排查项 | 结果 |
|--------|------|
| `~/.workbuddy/workbuddy.db` 中 217 个会话，cwd / title 匹配 `%qianfan%`/`%dumate%`/`%DuMate%` | **0 行** |
| 同上，`id LIKE 'ses_%'` | **0 行** |
| `~/.workbuddy/traces` 全量 1165 个 trace | 无 `ses_` 形态 sessionId；`agentName` 仅 `cli / terminalTitleGenerator / contextSummary / enhance-prompt` 四种；`metadata` 全空 |
| 百度搭子自有数据 | 在 `~/.qianfan/workspace/sessions/<uid>/<date>/<chat>/.dumate/ses_*/flows/*.yml`，是**非本技能 trace schema** 的 yml 流转格式，**无映射** |
| 客户端本体 | `%LOCALAPPDATA%\Programs\DuMate\DuMate.exe`，**没有** AppData / Roaming 数据目录 |

结论：`--source dumate` 跑出的 16 个会话 / 161 条 trace **100% 是 WorkBuddy 的**。
问题不是「共用目录导致归因模糊」，而是**空数据贴了来源标签**——旧版本文档里写的
「与 WorkBuddy 完全一致（实测，2026-10-02）」属于过度断言：当时只观察过
「路径常量指向这里」，并未验证归属，因此该表述已按本节口径改写。

**由此产生的行为约束（写报告 / 对外分享时必须遵守）：**

1. 不得把 dumate 的用量、token、成本写成「百度搭子用量 / 百度搭子花费」这种
   结论式表述；报告里的「百度搭子使用情况报告」只是**入口标识**，不是归属声明；
2. 该适配器的正确定位是「**支持任何写入 WorkBuddy 布局目录的第三方客户端**
   的通用入口」，归属由使用者自行确认；
3. 若确需百度搭子自有数据，需先为 `.dumate/ses_*/flows/*.yml` 建立 trace schema
   映射（见 §7.1），并保留 `~/.qianfan` 的读取路径——那是**另一件事**，本适配器没做；

**其他边界：**

- 产出 / 记忆日志的会话目录按 WorkBuddy 约定在 `DUMATE_OUTPUTS_DIR`
  （默认 home 的同级 `WorkBuddy`）。它**不从 `Path.home()` 取**，否则
  `DUMATE_HOME` 指到临时目录时 outputs / memory_logs 仍会读回用户真实目录
  （audit hook 实测抓到 17 次真实 HOME 访问）；
- `workbuddy.db` 以**只读**方式打开（`mode=ro`）——WAL 模式下可写连接会额外
  创建 `-wal` / `-shm`，且客户端持锁时会 `SQLITE_BUSY`；
- 若该客户端未来改用独立目录，需同步更新 `adapters/dumate.py` 的
  `_child_paths()` / `_resolve_outputs_dir()` 与 `_PATH_ATTRS`。

---

## 七、新增一个 Agent

### 7.1 需要新增的组件

1. **采集适配器** `adapters/<agent>.py`

   提供统一入口，返回 `(traces, db_data)`：

   ```python
   def collect_<agent>(start_date: str, end_date: str, **kw):
       """返回 (traces: list[dict], db_data: {"sessions": list[dict]})"""
   ```

   - `traces` 每项须含：`date` / `session_id` / `total_tokens` / `input_tokens` /
     `output_tokens` / `cached_tokens` / `effective_tokens` / `total_cost` /
     `effective_cost` / `channel` / `raw_model` / `exec_model` / `is_free`
   - `db_data["sessions"]` 每项须含：`id` / `cwd` / `title` / `created_date` /
     `mode` / `model` / `_dialogue_text`（任务分类依赖它）

2. **计价**：把该 Agent 的模型单价写进 `scripts/pricing.json`（发布版）或让用户写
   `scripts/pricing.local.json`；新增通道前缀时在 `ca_core.parse_channel()` 与
   `price_of()` 各加一个分支。

3. **CLI 分发**：`scripts/collect_usage_data.py` 的 argparse `--source` 增加取值，
   `main()` 增加分支调用适配器；其余聚合与渲染逻辑无需改动。

4. **（可选）计费能力声明** `SUPPORTS_COST`
   模块级常量，缺省视为 `True`。若该 Agent 按积分 / 订阅计费、金额无法归因到单个会话
   （千问办公就是），显式写 `SUPPORTS_COST = False`：采集器会把 `meta.cost_supported=false`
   落进数据文件，报告端据此**永久压制**「缺失单价模型 + `pricing.local.json` 补价 stub」整块，
   避免引导用户去填一个算不出真实金额的价。
   **不要靠「单价全是 0」隐式推断** —— 那样将来该源真出可计价套餐时还得回头改渲染层。

5. **（可选）维度与结构声明**，同样「显式优于隐式」，采集器算好后并入 `meta`：

   | 字段 | 含义 | 不给会怎样 |
   |---|---|---|
   | `single_channel` | 该源只有一层通道（档位即入口），§3.2 与 §3.1 必然同构 | 渲染端只能靠「两表行数相等」猜，且换源就失效 |
   | `background_runs` | 后台自动运行摘要（次数 / 失败数 / 耗时 / 类型），**不进 `automation_runs`** | §八 会出现一堆归因不上的 unknown 组 |
   | `skill_usage_source` / `outputs_source` | 技能与交付物各自的**权威源**标注 | 报告读者无法判断这格数字从哪来（如累计表 vs 转录） |

   技能 / 交付物 / 自动化三件事在每个 Agent 上的落点都不同，**必须实测该 Agent 的本机数据**
   再决定「采什么、显示什么、留空什么」——千问办公这一轮的初判就是把「我没采」误写成
   「该源没有」，参见 §4.6。

### 7.2 验收清单

- [ ] `adapters/<agent>.py` 能读取该 Agent 用量并归一化为统一 schema
- [ ] 技能 / 交付物 / 自动化三维度各自**实测过本机数据落点**，采到就出、真没有就是 0，
      不许用「不适用」话术掩盖未采
- [ ] 该 Agent 的模型单价可查（发布版或本地覆盖）
- [ ] `--source <agent>` 端到端跑通一份报告
- [ ] `tests/test_<agent>_adapter.py` 通过：解析正确性、日期过滤、成本计算、健壮性、CLI 黑盒
- [ ] 更新 `SKILL.md` / `README.md` / 本文档的「支持范围」表格
- [ ] 测试通过 `CLAUDE_PROJECTS_DIR` 之类的环境变量把 fixture 指向 `tmp_path`，**绝不读取用户真实目录**
