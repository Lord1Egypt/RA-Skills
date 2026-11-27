---
name: agent-worklog-review
description: 盘点本机所有 AI Agent 的会话记录，提取并分类完成的工作任务，统计 token 消耗，生成汇报材料。当用户要求"整理我在各 agent 完成的工作""统计 AI 工具使用情况""盘点对话记录""生成 AI 落地汇报材料""整理周会/述职 AI 工具应用成果"时使用。纯本地只读，不联网、不上传对话内容。
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    envVars:
      - name: WORKLOG_CONFIG
        required: false
        description: 项目分类规则 JSON 路径；未设置时用内置通用规则
      - name: WORKLOG_WSL_USER
        required: false
        description: WSL 用户名（非常规用户名时指定，避免自动探测不到）
      - name: WORKLOG_WSL_DISTRO
        required: false
        description: WSL 发行版名（非常规环境时指定）
      - name: WORKLOG_EXTRA_ROOTS
        required: false
        description: 额外会话库根目录，多个用分号或逗号分隔
      - name: WORKLOG_PROMPT
        required: false
        description: 设为 1 开启交互提示；仅在 stdin 是 TTY 时生效
      - name: WORKLOG_OUT_DIR
        required: false
        description: 输出目录，默认 Skill 根目录下的 output/
      - name: WORKLOG_NOISE_FILTERS
        required: false
        description: 噪音过滤规则 JSON 路径，过滤被误判为任务的注入文本
      - name: WORKLOG_ADAPTER_RULES
        required: false
        description: L2 声明式适配器规则 JSON 路径，用于零代码接入新 Agent
---

# Agent 工作台账盘点（agent-worklog-review）

盘点本机所有 AI Agent 的会话记录，产出「完成了什么工作、用了哪些工具、消耗多少 token」的结构化证据链，用于周会汇报、述职、AI 落地成效总结。

## 铁律（必须遵守）

1. **只读、本地、不外发**：全程只读取本机会话文件；**禁止**把对话正文、代码、密钥上传到任何网络服务或外部 API。
2. **会话量 ≠ 工作量**：报告中必须标注口径——含 Agent 自评估/自动化测试会话，不代表人工工作量。汇报时说"AI 辅助会话记录"，不要说"完成任务数"。
3. **不修改原始记录**：所有输出写到 `output/` 目录，绝不改动任何 agent 的原始会话文件。
4. **环境缺失静默跳过**：同事可能只有 Cursor、没装 WSL、没有 conda。脚本自动探测到什么算什么，缺的跳过，不报错中断；报告只列本机实际在用的 Agent，未安装的不列入。

## 核心设计：适配器架构（v2）

扫描层（`scan_agents.py`）能发现 26+ 种 Agent；**数据提取层**由 `scripts/adapters/` 下的插件负责，每个 Agent 一个文件。**新增 Agent 只需加一个适配器文件，不用改任何核心脚本**，`run_all.py` 会自动发现。

当前内置适配器（21 个，L1 专用）：

| 适配器 | Agent | 任务提取 | Token 统计 | 验证状态 |
|---|---|---|---|---|
| `workbuddy.py` | WorkBuddy | sessions 表 | session_usage 表 | ✅ 已验证 |
| `codex.py` | OpenAI Codex | rollout jsonl | token_count 事件 | ✅ 已验证 |
| `claude.py` | Claude Code | projects jsonl | message.usage | ✅ 已验证 |
| `dsh.py` | dsh | projcache + zstd 正文（每会话仅最新 generation） | zstd usage（需 zstandard） | ✅ 已验证 |
| `qoder.py` | Qoder | *-session.json | total_*_tokens | ✅ 已验证 |
| `vscdb.py` | Cursor / Trae / CodeBuddy / Windsurf / MarsCode | state.vscdb（cursorDiskKV） | ❌ tokenDetails 多为空 | ✅ 已验证 |
| `aider.py` | Aider | .aider.chat.history.md | ❌ 无 token 字段 | ✅ 已验证 |
| `opencode.py` | opencode | storage/message/*.json | tokens 字段（有则取） | ✅ 已验证 |
| `openakita.py` | OpenAkita | conversation_history | ❌ 无 token 字段 | ✅ 已验证 |
| `kimi.py` | Kimi Code | context.jsonl / user-history / **wire.jsonl** | **wire.jsonl StatusUpdate**（每会话取最终快照） | ✅ 已验证 |
| `zcode.py` | ZCode（智谱） | `~/.zcode/cli/db/db.sqlite` → model_usage | input/output/cache_*_tokens | ⚠️ 路径来自 ccusage，未验证 |
| `copilot.py` | GitHub Copilot CLI | `~/.copilot/otel/*.jsonl` + `session-state/*/events.jsonl` | ❌ 无可靠 token | ⚠️ 路径来自 ccusage，未验证 |
| `openclaw.py` | OpenClaw | `sessions/**/*.jsonl` + `openclaw-agent.sqlite` | `message.usage.input/output` | ⚠️ 路径来自 ccusage，未验证 |
| `hermes.py` | Hermes Agent | `~/.hermes/state.db` → sessions 表 | input/output/cache_*_tokens | ⚠️ 路径来自 ccusage，未验证 |
| `qwen.py` | Qwen Code | `~/.qwen/projects/*/chats/*.jsonl`（含 archive） | `usageMetadata.*TokenCount` | ⚠️ 路径来自 ccusage，未验证 |
| `kiro.py` | Kiro | ~/.kiro 会话 | ❌ 无 token | ⚠️ 按公开格式，未验证 |
| `roo.py` | Roo Code | ~/.roo 会话 | ❌ 无 token | ⚠️ 按公开格式，未验证 |
| `gemini_cli.py` | Gemini CLI | `~/.gemini/tmp/*/chats/*.json\|jsonl` | usageMetadata | ⚠️ 路径来自 ccusage，未验证 |
| `amp.py` | Amp | ~/.amp 会话 | ❌ 无 token | ⚠️ 按公开格式，未验证 |
| `augment.py` | Augment Code | ~/.augment 会话 | ❌ 无 token | ⚠️ 按公开格式，未验证 |
| `heuristic.py` | L3 兜底（见下） | 通用解析未覆盖 agent | ❌ 不提取 | 兜底机制 |

> ⚠️ 标注「未验证」表示本机未安装该 Agent、未用真实会话验证；其中 ZCode/Copilot/OpenClaw/Hermes/Qwen/Gemini 的**路径与字段名来自 ccusage 权威实现**（`rust/adapters/*/src/paths.rs` 等），不再是猜测。跑完若为 0 任务，可能只是本机没装；按 L2 规则补路径即可。

## 三层覆盖机制（新增 Agent 不必写 Python）

| 层 | 机制 | 适用场景 | 报告标注 |
|---|---|---|---|
| **L1 专用适配器** | `scripts/adapters/*.py`，精确解析 | 格式已知且验证过 | ✅ 专用适配器已覆盖 |
| **L2 声明式通用适配器** | `config/local/adapter_rules.local.json` 加一条规则 | 新 Agent、格式简单（JSONL/JSON/MD） | ⚠️ 通用兜底提取（需人工核验） |
| **L3 启发式兜底** | `heuristic.py` 自动扫描 L1/L2 未覆盖的 agent | 完全没适配器的冷门 Agent | ⚠️ 通用兜底提取（需人工核验） |

**输出只含本机实际产生会话数据的 Agent**（`common.py` 的 `installed_agents()`：任务/token 文件里出现过的 agent）。扫描到目录但没数据、或本机根本没装的 Agent（ZCode/Hermes/OpenClaw 等）一律不进报告——不给同事制造"我漏统计了"的噪音。真在用但没匹配上适配器的，才由 L3 兜底并标注需人工核验。

**L2 用法**：复制 `config/adapter_rules.example.json` 为 `config/local/adapter_rules.local.json`，在 `rules` 数组里加一条：

```json
{
  "name": "MyAgent",
  "dir_patterns": [".myagent/sessions/*"],
  "file_globs": ["*.jsonl"],
  "data_style": "jsonl",
  "token_spec": null
}
```

- `data_style`：`jsonl` / `json` / `json-array` / `flat-text`
- `token_spec`：不填或 `null` 表示不暴露 token（如实标注）；有 token 则填 `{"input": [...], "output": [...], "total": [...]}`
- 也可设 `WORKLOG_ADAPTER_RULES` 指向任意规则文件
- 保存后重跑 `run_all.py` 即可纳入，无需改任何脚本

## 使用场景

- "整理我在 Claude Code / Codex / dsh / Cursor 里做完的工作"
- "统计今年 AI 工具用了多少 token"
- "周会要汇报 AI 落地情况，帮我出材料"
- "看下本机装了哪些 agent，对话记录在哪"

## 工作流

### Step 0：确认输出目录与配置

- 输出默认在 Skill 根目录的 `output/`，可通过环境变量 `WORKLOG_OUT_DIR` 覆盖。
- **项目分类规则**（可选）：把 `config/project_rules.json.example` 复制为 `config/local/project_rules.local.json` 并填入自己的项目名与关键词正则；也可设 `WORKLOG_CONFIG=/path/to/rules.json`。**不配置也能跑**：用通用规则 + 从工作目录末级目录名推断项目。
- **噪音过滤**（可选）：把 `config/noise_filters.example.json` 复制为 `config/local/noise_filters.local.json`，填入本机会话里被误判为任务的注入文本样本。
- **新 Agent 适配**（可选）：本机有未覆盖的 Agent 时，复制 `config/adapter_rules.example.json` 为 `config/local/adapter_rules.local.json` 加规则（见「三层覆盖机制」），无需写 Python。
- **WSL 特殊用户名**（可选）：若 WSL 用户名/发行版非常规，设 `WORKLOG_WSL_USER` / `WORKLOG_WSL_DISTRO` 环境变量。

### Step 1：一键执行

```bash
python scripts/run_all.py                      # 默认静默，后台/CI 安全
python scripts/run_all.py --interactive        # 非常规环境时交互式补问
```

**交互模式（可选）**：默认静默跳过缺失项；加 `--interactive`（或 `WORKLOG_PROMPT=1`）后，遇到非常规环境会提示输入。仅在 stdin 是 TTY 时生效，后台跑不会卡住。提示项：

| 触发条件 | 提示内容 |
|---|---|
| WSL 自动探测为空且未设环境变量 | 输入 WSL 用户名 / 发行版名 |
| 无项目规则配置 | 输入要重点统计的项目名（逗号分隔） |
| 某 Agent 有目录但无会话文件 | 输入非标准会话库根目录 |

每项都可回车跳过；只问用户名/路径/项目名，**从不超过问 token/密钥**。环境变量 `WORKLOG_WSL_USER` / `WORKLOG_WSL_DISTRO` / `WORKLOG_EXTRA_ROOTS` 已设置时不再重复问。

脚本自动完成 6 步：
1. 独立进程探测 WSL 路径（带超时，避免 UNC 卡死）→ 写 `_env_paths_cache.json`
2. `scan_agents.py` — 全盘扫描 agent 及会话存储位置
3. `extract_tasks.py` — 遍历所有适配器提取任务（含 dsh zstd 解压正文）
4. `classify_tasks.py` — 按项目 / 工作类型 / AI 技能标签 / 月份多维分类
5. `stat_tokens.py` — 遍历所有适配器统计 token，再刷新报告
6. `export_excel.py` — 导出多 sheet Excel 工作簿（含缓存率与可选费用列）

**环境要求**：Python 3.8+（主链路仅标准库）。可选依赖：
- `zstandard`：dsh 压缩会话统计；脚本自动探测带该模块的解释器（含 conda），找不到则跳过并在报告标注。
- `openpyxl`：Excel 导出；缺失时只打印提示并跳过，**不影响前面 5 步产物**。
如需费用列，把定价表放 `config/local/pricing.local.json`（`{"模型名":{"input":单价,"output":单价,"cache":单价}}`），不配置就不臆造价格。

### Step 2：检查产出

`output/` 下生成：

| 文件 | 内容 |
|---|---|
| `agent_scan_report.json` | 所有 agent 的安装目录与会话存储位置 |
| `all_tasks.jsonl` | 原始提取任务（agent/标题/时间/路径/轮次） |
| `tasks_classified.jsonl` | 带分类标签的结构化任务 |
| `task_analysis_report.md` | 多维分类报告 + 核心发现 + **本机在用 Agent 表** + Agent×项目交叉表（只列实际产出数据的 Agent） |
| `token_usage.jsonl` | 会话级 token 明细 |
| `token_report.md` | token 汇总报告（按 Agent/项目/月份/模型）+ **未纳入统计说明**（只列在用但无 token 的 Agent） |
| `agent_worklog.xlsx` | 11 sheet Excel：总览/按Agent/按项目/按月份/按模型/Top会话/4张任务分类表/任务明细；含**缓存率**与可选费用列 |

### Step 3：生成汇报材料

基于 `task_analysis_report.md` + `token_report.md`，按 `templates/汇报材料模板.md` 生成一页纸材料。要点：

- **工具矩阵**：用了哪些工具、各用在什么项目（用交叉表）
- **全流程场景**：需求→设计→编码→Review→测试→运维→文档，每环节举 1-2 个真实任务
- **落地成效**：用 **非缓存 token** 口径 + 质量治理类任务占比
- **沉淀推广**：Skill 数、复用、团队覆盖
- **边界与问题**：主动讲 AI 局限与安全合规（内网部署、数据不出域）

## 关键口径（写报告时必须带上）

| 口径 | 含义 | 用法 |
|---|---|---|
| 合计 token | 含缓存命中，会被放大（Codex 缓存占比约 97%） | 讲"处理规模" |
| 非缓存 token | (input − cached) + output，接近实际计费 | 讲"真实用量"，更经得起追问 |
| 缓存率 | cache_tokens / total_tokens × 100%（Excel 中各维度表均含） | 说明上下文复用比例，解释合计 token 为何被放大 |
| 会话数 | 含 Agent 自评估/自动化测试 | 讲"AI 辅助记录"，不等于人工工作量 |
| 费用 | 仅在配置了 `pricing.local.json` 时按单价估算 | 不配置就不出数字，不臆造价格 |

## 扩展：为新 Agent 接入（按成本从低到高）

1. **零代码（推荐）**：加 L2 声明式规则，见上文「三层覆盖机制」，改 JSON 即可。
2. **半代码**：继承 `scripts/adapters/_declarative.py` 的 `DeclarativeAdapter`，只声明 `dir_patterns` / `file_globs` / `data_style` / `token_spec` 类属性，几行搞定（参考 `zcode.py` / `qwen.py`）。
3. **完全自定义**：复制 `scripts/adapters/_TEMPLATE.py` 为 `<agent名>.py`，改类名与 `name`，实现 `extract_tasks()` / `collect_tokens()`，用 `all_homes()` / `appdata_roots()` / `find_files()` 找文件（勿写死用户名和路径）。保存后无需改核心脚本，重跑 `run_all.py` 即可纳入。
4. **兜底**：什么都不做，L3 `heuristic.py` 会对未覆盖 agent 通用提取，报告标注 `source=heuristic` 提示人工核验。

**注意**：
- 拿不到 token 就返回 `[]` 并设 `token_available=False` + `token_note`，报告会如实标注，绝不伪造。
- 避免全 home 无限递归（会扫到 node_modules / WSL UNC 卡死），限制深度或限定候选目录。
- 未验证的适配器设 `verified=False`（或 L2 规则里 `"verified": false`）；这类 Agent 本机没装时**不进报告**，只有实际产出数据后才会出现（届时应补真实会话验证）。
- L3 启发式适配器必须最后执行：`extract_tasks.py` 里按 name 排序保证它在末尾，因为它要读扫描报告并排除已覆盖 agent。

## 踩坑记录（改造脚本前务必读）

1. **WSL UNC 卡死**：`os.listdir('\\\\wsl.localhost')` 在 Anaconda Python 下会长时间卡死；UNC `os.path.isdir` 也可能不稳定。解决：`probe_wsl.py` 独立进程 + 40s 超时探测，结果写 `_env_paths_cache.json`，其余脚本只读缓存不碰 UNC 列举。
2. **UNC 双前缀重复**：`\\wsl.localhost` 与 `\\wsl$` 指向同一文件，每种发行版只保留一种前缀，否则 token 翻倍。
3. **WSL 用户名写死**：不要写死用户名列表，用 `WORKLOG_WSL_USER` 环境变量 + 常见名候选。
4. **UUID 命名会话**：Claude / Codex 会话文件是纯 UUID，按所在目录判定 + 扩展名过滤，不能只靠文件名正则。
5. **压缩会话**：dsh `.zstd` 是流式压缩，必须 `ZstdDecompressor().stream_reader()`；用户消息藏在 `agent/inbox/spliced` 的 `data.inserted[].content[].text`。
6. **数据库型会话**：WorkBuddy 在 `workbuddy.db` 的 `sessions`/`session_usage` 表；Cursor 在 `state.vscdb` 的 `cursorDiskKV` 表（`composerData:*`，`conversation[].text`，type 1=用户）。
7. **Claude 消息重复**：同一 `message.id` 会在 jsonl 里重复写入，token 统计必须去重。
8. **Codex 缓存重复计入**：`cached_input_tokens` 是 `input_tokens` 子集，非缓存 = (input − cached) + output，total 用数据源的 `total_tokens`。
9. **系统注入过滤**：Codex 大量会话首条是环境注入文本，用 `load_noise_markers()` 过滤；本机特有样本放 `config/local/noise_filters.local.json`，不写死在代码里。
10. **token 不去重 session_id**：resume 会产生多个 rollout 文件，每个是独立时间段的累计快照，去重会丢失大量 token（实测 197 亿 → 57 亿）。
11. **全 home 递归卡死**：Aider/OpenAkita 若 `find_files([home], ...)` 会递归到 AppData/WSL 卡死，必须限制深度 + 跳过噪声目录。
12. **交互提示必须 TTY 守卫**：`ask()` 同时检查 `WORKLOG_PROMPT` 开关和 `sys.stdin.isatty()`，两个都满足才提示；后台/CI 跑即便设了开关也不会卡住。交互模式下 `probe_wsl.py` 不能 `capture_output=True`，否则用户看不到提示。
13. **L3 启发式必须最后跑**：`heuristic.py` 要读 `agent_scan_report.json` 并排除已被 L1/L2 覆盖的 agent，`extract_tasks.py` 里显式把它排到末尾，否则会与专用适配器重复统计。
14. **声明式基类的 token_spec 不能想当然**：未验证的 agent（ZCode/Gemini CLI 等）即使填了 token 字段映射，字段也可能不存在；`find_token` 找不到时返回 0，报告会显示该 agent 0 token——这是如实反映，不是 bug。拿不准就设 `token_spec: null` 更诚实。
15. **Kimi Code 的 user-history 是纯 content**：`~/.kimi/user-history/*.jsonl` 每行只有 `{"content":...}` 无 role 字段；`context.jsonl` 才有 role。`kimi.py` 对两种情况都做了兼容，并过滤 `/login`、`/model` 等命令类输入。
16. **Kimi token 在 wire.jsonl 不在 context.jsonl**：`message.type=StatusUpdate` → `payload.token_usage.{input_other, output, input_cache_read, input_cache_creation}`；用户消息在 `TurnBegin.payload.user_input[].text`。**StatusUpdate 是会话累计快照**（同一会话 20 条 input 递增），逐条累加会虚高，必须每会话只取最后一条。
17. **dsh 多 generation 是同一会话副本**：`session.jsonl`=gen0，`session.vN.jsonl[.zstd]`=genN；只取每目录最大 generation，否则重复计入（本机实测 65 个 zstd 中 4 个是旧版）。
18. **未验证 Agent 的路径优先查 ccusage 源码**：`rust/adapters/<agent>/src/paths.rs` 与 `loader.rs` 给出准确路径和 SQLite 表结构（ZCode `~/.zcode/cli/db/db.sqlite` 的 `model_usage`+`session`；Hermes `~/.hermes/state.db` 的 `sessions`；OpenClaw `transcript_events` 的 `event_json`）。不要靠猜目录。
19. **月份必须用 `month_of()`**：token 时间戳既有 ISO 字符串也有 10/13 位 Unix 秒/毫秒，直接 `str(ts)[:7]` 会产生 190+ 个假月份。
20. **报告只列在用 Agent**：`installed_agents()` 从 `all_tasks.jsonl`+`token_usage.jsonl` 取实际产出数据的 agent，配合 `norm_agent()` 统一别名（Codex/OpenAI Codex、Cursor/Trae/CodeBuddy 等）。适配器清单里"按公开格式未验证"的 Agent（ZCode/Hermes/OpenClaw 等）本机没装就不进报告——扫描到目录残留（如 OpenClaw 1 个文件）也不算在用，避免误判为"漏统计"。
20. **Excel 费用列不许臆造**：只有用户放了 `config/local/pricing.local.json` 才算费用；没有就留空并注明，不用内置价格表误导。

## 目录结构

```
agent-worklog-review/
├── SKILL.md
├── scripts/
│   ├── common.py              # 环境探测、路径缓存、时间戳、zstd 探测
│   ├── probe_wsl.py           # 独立进程探测 WSL 路径（带超时）
│   ├── scan_agents.py         # 全盘扫描
│   ├── extract_tasks.py       # 任务提取调度器（遍历适配器）
│   ├── stat_tokens.py         # token 统计调度器（遍历适配器）
│   ├── classify_tasks.py      # 多维分类
│   ├── export_excel.py        # ★ 多 sheet Excel 导出（缓存率/可选费用）
│   ├── run_all.py             # 一键串联（6 步）
│   └── adapters/              # ★ 插件目录：每个 Agent 一个适配器
│       ├── base.py            # 基类 + 工具函数 + 自动发现 + L2 动态加载
│       ├── _TEMPLATE.py       # 完全自定义适配器模板
│       ├── _jsonutil.py       # 通用 JSONL/JSON 解析工具（内部）
│       ├── _declarative.py    # L2 声明式基类（内部）
│       ├── workbuddy.py / codex.py / claude.py / dsh.py
│       ├── qoder.py / vscdb.py / aider.py / opencode.py / openakita.py / kimi.py
│       ├── zcode.py / copilot.py / openclaw.py / hermes.py / qwen.py
│       ├── kiro.py / roo.py / gemini_cli.py / amp.py / augment.py
│       ├── generic.py         # L2：从配置动态生成适配器
│       └── heuristic.py       # L3：未覆盖 agent 的启发式兜底
├── config/
│   ├── project_rules.json.example   # 项目分类规则模板
│   ├── noise_filters.example.json   # 噪音过滤模板
│   ├── adapter_rules.example.json   # ★ L2 新 Agent 声明规则模板
│   └── local/                       # 本机私有配置（分发时不带）
│       ├── project_rules.local.json
│       ├── noise_filters.local.json
│       ├── adapter_rules.local.json
│       └── pricing.local.json   # 可选：模型单价表（不配则不出费用列）
└── templates/
    └── 汇报材料模板.md
```
