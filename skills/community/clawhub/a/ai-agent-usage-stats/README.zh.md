# agent-usage-stats — AI Agent Token 消耗统计工具

[中文](README.md) | [English](README.en.md)

统计本机 AI 编程助手的 token 消耗，支持多 Agent、多模型、多时间段查询与导出。

## 为什么选择 agent-usage-stats

`agent-usage-stats` 直接读取本地数据，跨 Agent、跨模型、跨平台运行。零依赖，纯 Python 标准库。

| 功能 | 命令 | 说明 |
|------|------|------|
| **Token 消耗统计** — 指定时间范围 | `agent-usage-stats -a claude-code --month` | 多 Agent（Claude Code / CodeX / Hermes / OpenClaw / Reasonix / DeepSeek TUI）、多模型，输入/输出/缓存 token 和调用次数，有数据才展示 |
| **实时监控** — 上下文占比追踪 | `agent-usage-stats -a claude-code --watch` | 每轮增量 + 累计量，超 90% 预警，macOS / Linux / Windows 通用 |
| **时段对比** — 两个时间段并排比较 | `--compare --a yesterday --b today` | 任意时间段聚合，多模型横向对比，带差值列 |
| **数据导出** — XLSX / JSON | `--export` | 多 Agent、多时间段组合，交互式选目录；年度按月拆分 |
| **模型识别** — 中转站 API 校验 | `agent-usage-stats -a <name>` | 自动识别 API 返回的模型名称（69 个模型 13 个厂商） |

---

## 环境要求

安装前需满足以下环境要求：

### 1. Python 3.11+

`agent-usage-stats` 本身是纯 Python 脚本，依赖标准库（含 `tomllib` 用于模型价格配置），不需要额外 pip 装任何包。

```bash
# 检查已安装（Windows 用户用 python --version）
python3 --version

# 如未安装 → https://www.python.org/downloads/
```

### 2. Node.js（安装工具时需要）

`agent-usage-stats` 通过 **ClawHub CLI** 安装。ClawHub 是个 Node.js 命令行工具。

```bash
# 检查已安装
node --version

# 如未安装 → https://nodejs.org（选择 LTS 版本）
```

装好 Node.js 后会自动带上 `npm`，用来装 ClawHub。

### 3. ClawHub CLI

```bash
# 安装（npm 全局安装）
npm install -g clawhub

# 验证
clawhub -V          # 显示版本号
```

> 💡 如果你用的是 macOS 且通过 Homebrew 装过 Node.js，
> `npm install -g clawhub` 安装后会出现在 `/opt/homebrew/bin/clawhub`，
> 通常已经在你 PATH 里了，直接用就行。

---

### 数据范围

> ⚠️ `agent-usage-stats` **仅统计本机数据，不跨机器汇总**。
>
> - **同一把 API Key 用在多台机器 → 每台机器的统计互不相通**
> - 例：API Key 同时在 PC A 和 PC B 用，PC A 的 `agent-usage-stats` 只看得到 PC A 的用量
> - `agent-usage-stats` 不联网、不查 API 后台，纯读本地磁盘文件
> - 要看另一台机器的统计，请在那台机器上也安装 `agent-usage-stats`
>
> 🕐 **时区说明**：`--today` / `--yesterday` 等时间段基于**本机系统时区**。例如北京时间 (UTC+8) 的 `--today` 统计范围为当日 00:00~23:59 CST。跨时区机器看到的数据范围不同。

### API 中转站

通过中转站访问大模型时，统计准确性取决于中转站是否**原样透传** API 返回的 `usage` 字段。`agent-usage-stats` 只记录 Agent 本地写入的数据，不校验与上游 API 是否一致。

### 统计原理

`agent-usage-stats` 读取各 Agent 写入本地的数据文件（SQLite / JSONL），按模型聚合 `usage` 对象中的 `input_tokens`、`output_tokens`、`cache_read_tokens` 和调用次数。数据链路：

```
API 返回 usage → Agent 写入本地 → agent-usage-stats 读取汇总
```

统计结果可能与 API 结算后台存在偏差，原因：
- **缓存 token 叠加**：`cache_read_tokens` 可能被多次计入（每轮缓存命中都计数）
- **Agent 未完整记录**：部分 Agent/版本不记录 `tool_call_count` 等字段
- **时区差异**：API 后台使用 UTC，本工具使用本地时区
- **中转站改写**：中转站可能修改或移除 `usage` 字段

> 本工具定位为**本地账本**，呈现的是 Agent 记录的数据，非上游结算依据。

### 缓存命中率

**通用公式**：`cache_read_tokens / (cache_read_tokens + cache_creation_tokens) × 100%`

所有参与缓存系统的 prompt tokens 中，命中缓存（直接从缓存读取）的比例。

**agent-usage-stats 计算方式**：各 Agent 底层 API 不同，采用自适应公式：

```
如果 cache > input:  缓存率 = cache / (cache + input)   ← DeepSeek API（input = cache_miss）
如果 cache ≤ input:  缓存率 = cache / input              ← 标准 API（input = 总 prompt）
```

| Agent | 数据来源 | 精确度 |
|-------|---------|:---:|
| Reasonix | `cacheHitTokens` + `cacheMissTokens` 均已知 | 精确 |
| Claude Code / Hermes / OpenClaw | `cache_read_input_tokens`（无 creation） | 近似(偏保守) |
| CodeX / DeepSeek TUI | 无缓存数据 | 不展示 |

- `cache = 0` 时不展示缓存率
- 对于 Anthropic API，`input_tokens` 包含不参与缓存的 tokens，实际命中率略高于展示值
- 监控模式增量段的缓存率表示该时间窗口内的命中比例

### 预估费用

**配置文件**：项目根目录 `model_prices.toml`，覆盖 60+ 模型 14 个厂商。以模型名为 key（含点号的模型名需用引号包裹如 `["gemini-2.5-pro"]`），每模型配置三个价格字段：

| 字段 | 含义 | 单位 |
|------|------|------|
| `input_no_cache_price` | 输入 token 单价（缓存未命中） | 每百万 (1M) tokens |
| `input_cache_price` | 输入 token 单价（缓存命中） | 每百万 (1M) tokens |
| `output_price` | 输出 token 单价 | 每百万 (1M) tokens |

所有模式默认展示预估费用（有价格则显示 `≈¥X.XX`，无价格显示 `-`）。

**计价公式（与缓存率逻辑一致，自适应两种 API 模式）**：

```
# 标准 API（cache ≤ input，input = 总 prompt = cacheHit + cacheMiss）
no_cache    = input - cache      # 未命中缓存的部分
cache_tokens = cache             # 命中缓存的部分

# DeepSeek API（cache > input，input = cacheMiss 不含 cacheHit）
no_cache    = input              # input 本身就是 cacheMiss
cache_tokens = cache             # cache 就是 cacheHit

# 统一公式
费用 = (no_cache × input_no_cache_price
     +  cache_tokens × input_cache_price
     +  output × output_price) / 1,000,000
```

> 例：DeepSeek API 下，`input=570K`（cacheMiss），`output=25K`，`cache=4.28M`（cacheHit），deepseek-v4-flash 价格（no_cache=¥1.0, cache=¥0.02, output=¥2.0）。
> 费用 = `(570000 × 1.0 + 4280000 × 0.02 + 25000 × 2.0) / 1,000,000` = `(570000 + 85600 + 50000) / 1M` = **≈¥0.71**

**监控模式计价**：每轮刷新时计算增量费用。以初始快照为基线，当前累计减去基线得到各模型增量 token（Δinput/Δoutput/Δcache），代入公式求和即为本轮增量费用。停止时展示「监控期间增量」费用合计。

**混币统一**：USD 定价模型按汇率 7.25 自动转为人民币展示，最终统一为 `≈¥X.XX`。

**价格匹配**：先精确匹配模型名，失败时按最长前缀匹配（如 `deepseek-v4-pro-20250219` → `deepseek-v4-pro` 价格）。

> ⚠️ **费用为预估值**：
> - 缓存未中 token（`cache_creation`）在部分 API 中未暴露，导致缓存命中率存在轻微低估，实际费用可能有小幅偏差
> - 未配置价格的模型（显示 `-`）不计入总计，多 Agent 合计行标注「仅供参考」
> - 请以 API 结算后台为准

## 安装

环境就绪后，执行以下命令完成安装：

**macOS / Linux：**
```bash
cd ~
clawhub install ai-agent-usage-stats
python3 ~/skills/ai-agent-usage-stats/agent-usage-stats.py setup
```

**Windows（PowerShell）：**
```powershell
cd ~
clawhub install ai-agent-usage-stats
python $HOME\skills\ai-agent-usage-stats\agent-usage-stats.py setup
```

> `cd ~` 确保技能安装到用户主目录（所有系统都有写入权限）。
> 如果 `python` 找不到，试试 `python3`（Microsoft Store 版 Python 用 `python3`）。
> 如果报错 `can't open file '...~...'`，参考：[PowerShell 路径展开问题](#ps-tilde)。
>
> `setup` 会自动将 `~/.local/bin` 加入系统 PATH，**需要新开一个终端窗口**才能生效。

安装完成后，新开终端即可使用 `agent-usage-stats` 命令。

### 验证安装成功

```bash
# 验证 1：版本号
agent-usage-stats --version
# 输出: agent-usage-stats v2.6.0

# 验证 2：看本机已安装的 Agent
agent-usage-stats --list-backends
# 输出示例:
#   ✅ Claude Code
#   ✅ CodeX
#   ✅ Hermes
#   ❌ OpenClaw
#   ✅ Reasonix
#   ✅ DeepSeek TUI

# 验证 3：直接看某个 Agent 的统计
agent-usage-stats -a claude-code
# 输出示例:
# 📊 Claude Code
#   Qwen3-Coder-30B-A3B-Instruct-MLX-4bit | 入 22.91K | 出 131     | 缓 0               | 总计/+缓存 23.04K/23.04K | 调用 1 次    | -
#   deepseek-v4-flash                     | 入 2.59M  | 出 102.93K | 缓 12.65M (83.0%)  | 总计/+缓存 2.69M/15.34M  | 调用 514 次  | ≈¥3.05
#   deepseek-v4-pro                       | 入 5.47M  | 出 1.57M   | 缓 588.81M (99.1%) | 总计/+缓存 7.04M/595.86M | 调用 3060 次 | ≈¥84.72
#   gemma-4-26B-A4B-it-MLX-4bit           | 入 89.18K | 出 1.08K   | 缓 0               | 总计/+缓存 90.26K/90.26K | 调用 4 次    | -
#   合计                                  | 入 8.18M  | 出 1.67M   | 缓 601.46M (98.7%) | 总计/+缓存 9.85M/611.31M | 调用 3579 次 | ≈¥87.77
```

以上三条均正常输出即表示安装成功。

## 更新

通过 ClawHub 更新到最新版本：

```bash
agent-usage-stats update
# 或
clawhub update ai-agent-usage-stats
```

> `update` 原地替换文件，包装器和 PATH 均无需重配。

> 💡 更新后版本没变？加 `--force` 强制拉取：
> ```
> clawhub install ai-agent-usage-stats --force
> ```

---

## 用法

### Agent 名称

`-a` / `--agent` 参数使用以下名称指定 Agent：

| 名称 | Agent | 说明 |
|------|-------|------|
| `claude-code` | Claude Code | Anthropic 官方 CLI |
| `codex` | CodeX | OpenAI Codex CLI |
| `hermes` | Hermes | 第三方 AI 编码助手 |
| `openclaw` | OpenClaw | 开源 AI 编程工具 |
| `reasonix` | Reasonix | 国产 AI 编码 CLI |
| `deepseek-tui` | DeepSeek TUI | DeepSeek 官方终端工具 |

示例：`agent-usage-stats -a claude-code --today`

### 快速参考

| 操作 | 命令 | 适用范围 |
|------|------|---------|
| 查看今日所有 Agent 统计 | `agent-usage-stats --all -t` | 所有 Agent |
| 查看本月统计 | `agent-usage-stats --all -m` | 所有 Agent |
| 查看单个 Agent | `agent-usage-stats -a claude-code` | 单个 Agent |
| 实时监控 | `agent-usage-stats -a claude-code -w` | 单个 Agent |
| 时段对比 | `agent-usage-stats -a claude-code --compare --a last-week --b this-week` | 单个 Agent |
| 导出数据 | `agent-usage-stats -a claude-code -m -e` | 单个/所有 Agent |
| 查看模型价格 | `agent-usage-stats --list-prices` | 配置查询 |
| 交互式菜单 | `agent-usage-stats` | 交互式选择 |

### 参数说明

| 短参数 | 长参数 | 说明 |
|:---:|---|---|
| `-a` | `--agent` | 指定 Agent，名称见上方 Agent 名称表。多个用逗号分隔 |
| `-t` | `--today` | 今日数据 |
| `-m` | `--month` | 本月数据（1 号至今） |
| `-y` | `--year` | 今年数据（1 月 1 日至今） |
| `-w` | `--watch` | 实时监控，默认 5 秒刷新，Ctrl+C 停止 |
| `-e` | `--export` | 导出为 XLSX / CSV / JSON |
| `-v` | `--version` | 查看版本号 |
| `-l` | `--list-backends` | 列出本机已安装的 Agent |
| | `--list-prices` | 列出 model_prices.toml 中已配置价格的模型 |
| `--all` | | 查看所有 Agent 统计 |

> 短参数可组合使用。例如 `-a claude-code -t -e` 表示导出 Claude Code 今日数据。

---

### 一、查看单个 Agent

以下示例以 Claude Code 为例，可替换为其他 Agent（`codex` / `hermes` / `openclaw` / `reasonix` / `deepseek-tui`）。

**直接看全部历史（不限时间段）：**

```bash
agent-usage-stats -a claude-code
```

**只看今天的：**

```bash
agent-usage-stats -a claude-code -t
```

**看昨天的：**

```bash
agent-usage-stats -a claude-code --yesterday
```

**看本月的（1 号到今天）：**

```bash
agent-usage-stats -a claude-code -m
```

**看今年的（1 月 1 号到今天）：**

```bash
agent-usage-stats -a claude-code --year
```

**看本周的（周一到今天）：**

```bash
agent-usage-stats -a claude-code --week
```

**看最近 7 天的：**

```bash
agent-usage-stats -a claude-code --last-7d
```

**自己指定日期范围：**

```bash
# 从 1 月 1 号到 5 月 18 号
agent-usage-stats -a claude-code --from 2026-01-01 --to 2026-05-18
```

输出示例：

```
📊 Claude Code
  deepseek-v4-flash | 入 2.59M | 出 102.93K | 缓 12.65M (83.0%) | 总计/+缓存 2.69M/15.34M | 调用 514 次 | ≈¥3.05
  deepseek-v4-pro   | 入 5.47M | 出 1.57M   | 缓 588.81M (99.1%) | 总计/+缓存 7.04M/595.86M | 调用 3060 次 | ≈¥84.72
  合计              | 入 8.18M | 出 1.67M   | 缓 601.46M (98.7%) | 总计/+缓存 9.85M/611.31M | 调用 3579 次 | ≈¥87.77
  ────────────────────────────────────
  子代理: 24 次 | 会话: 24 个 | 项目: 4 个
```

---

### 二、查看多个 Agent

**指定 Agent 列表（逗号分隔）：**

```bash
# 同时看 Hermes 和 Claude Code 本月的数据
agent-usage-stats -a hermes,claude-code -m
```

**一次性看电脑上所有 Agent 的数据：**

```bash
# 全部历史（不限时间段）
agent-usage-stats --all

# 所有 Agent 今天的数据
agent-usage-stats --all -t

# 所有 Agent 本月的数据
agent-usage-stats --all -m

# 所有 Agent 今年的数据
agent-usage-stats --all --year
```

输出示例：

```
📊 本机 Agent 统计汇总
══════════════════════════════════════════════════

✅ Claude Code
📊 Claude Code
  deepseek-v4-flash | 入 2.59M | 出 102.93K | 缓 12.65M (83.0%) | 总计/+缓存 2.69M/15.34M | 调用 514 次 | ≈¥3.05
  deepseek-v4-pro   | 入 5.47M | 出 1.57M | 缓 588.81M (99.1%) | 总计/+缓存 7.04M/595.86M | 调用 3060 次 | ≈¥84.72
  合计              | 入 8.18M | 出 1.67M | 缓 601.46M (98.7%) | 总计/+缓存 9.85M/611.31M | 调用 3579 次 | ≈¥87.77

✅ CodeX
📊 CodeX
  codex-auto-review | 总计 11.87K | 3 轮会话
  deepseek-v4-pro   | 4 轮会话
  gpt-5.4           | 总计 5.26M | 2 轮会话
  gpt-5.5           | 总计 26.59M | 4 轮会话
  合计              | 总计 31.86M | 13 轮会话

✅ Hermes
📊 Hermes
  deepseek-v4-flash | 上下文 92.42K/1.05M (8.8% ✅) | 入 83.5K | 出 8.92K | 缓 969.22K (92.1%) | 总计/+缓存 92.42K/1.06M | 调用 29 次 | ≈¥0.12

✅ Reasonix
📊 Reasonix
  deepseek-v4-flash | 入 189.67K | 出 4.93K | 缓 162.18K (85.5%) | 总计/+缓存 194.6K/356.77K | 调用 14 次 | ≈¥0.20

✅ DeepSeek TUI
📊 DeepSeek TUI
  deepseek-v4-pro | 总计 499.88K | 1 轮会话 | 工具调用 14 次 | ¥0.1477

══════════════════════════════════════════════════
  全部 Agent 总计
  入 40.81M | 出 1.69M | 缓 602.59M (93.7%) | 总计/+缓存 42.5M/645.09M | 调用 3636 次 | ≈¥129.40
```

---

### 三、列出本机已安装的 Agent

```bash
# 短参数
agent-usage-stats -l

# 长参数
agent-usage-stats --list-backends
```

输出示例：

```
本机已安装的 AI 助手：
  ✅ Claude Code
  ✅ CodeX
  ✅ Hermes
  ❌ OpenClaw
  ✅ Reasonix
  ✅ DeepSeek TUI
```

> ✅ = 已检测到，可查询。❌ = 未安装或无数据。

---

### 四、对比两个时间段

并排显示两个时间段的入/出/缓/缓存率/总计/总计(含缓存)/调用，带差值列。

**昨天和今天比：**

```bash
agent-usage-stats -a claude-code --compare --a yesterday --b today
```

**上周和这周比：**

```bash
agent-usage-stats -a claude-code --compare --a last-week --b this-week
```

**上个月和这个月比：**

```bash
agent-usage-stats -a claude-code --compare --a last-month --b this-month
```

**去年和今年比：**

```bash
agent-usage-stats -a claude-code --compare --a last-year --b this-year
```

**两个自定义日期比：**

```bash
# 两个具体的某一天
agent-usage-stats -a claude-code --compare --a 2026-01-01 --b 2026-01-15

# 两个日期范围（用 ~ 连接）
agent-usage-stats -a claude-code --compare --a 2026-01-01~2026-01-07 --b 2026-01-08~2026-01-14
```

支持的标签：`today` / `yesterday` / `this-week` / `last-week` / `this-month` / `last-month` / `this-year` / `last-year` / `YYYY-MM-DD` / `YYYY-MM-DD~YYYY-MM-DD`

输出示例：

```
📊 对比: 2026-05-22 vs 2026-05-23  [Claude Code]
=========================================================================
  模型              | 指标         | 2026-05-22 | 2026-05-23 | 变化
─────────────────────────────────────────────────────────────────────────
  deepseek-v4-flash | 入           | 0          | 570063     | +570.06K
                    | 出           | 0          | 25455      | +25.45K
                    | 缓           | 0          | 4281600    | +4.28M
                    | 缓存率       | -          | 88.3%      |
                    | 总计         | 0          | 595518     | +595.52K
                    | 总计(含缓存) | 0          | 4877118    | +4.88M
                    | 调用         | 0          | 165        | +165
  ·······································································
  deepseek-v4-pro   | 入           | 56667      | 424426     | +367.76K
                    | 出           | 8416       | 277165     | +268.75K
                    | 缓           | 549120     | 62059648   | +61.51M
                    | 缓存率       | 90.6%      | 99.3%      |
                    | 总计         | 65083      | 701591     | +636.51K
                    | 总计(含缓存) | 614203     | 62761239   | +62.15M
                    | 调用         | 18         | 456        | +438
  ·······································································
  合计              | 入           | 56667      | 994489     | +937.82K
                    | 出           | 8416       | 302620     | +294.2K
                    | 缓           | 549120     | 66341248   | +65.79M
                    | 缓存率       | 90.6%      | 98.5%      |
                    | 总计         | 65083      | 1297109    | +1.23M
                    | 总计(含缓存) | 614203     | 67638357   | +67.02M
                    | 调用         | 18         | 621        | +603
─────────────────────────────────────────────────────────────────────────
```

---

### 五、实时监控

按指定间隔刷新 token 消耗数据，支持增量展示和今日累计。Ctrl+C 停止后显示本次监控汇总。

**默认 5 秒刷新一次：**

```bash
agent-usage-stats -a claude-code -w
```

**自定义刷新间隔（比如 2 秒一次）：**

```bash
agent-usage-stats -a claude-code -w 2
```

输出示例：

```
📡 实时监控 [Claude Code] — 每 5 秒刷新 (Ctrl+C 停止)

初始状态:
  deepseek-v4-flash | 入 2.02M | 出 77.48K | 缓 8.36M | 总计/+缓存 2.1M/10.46M | 调用 349 次
  deepseek-v4-pro   | 入 4.9M  | 出 1.19M  | 缓 451.87M | 总计/+缓存 6.09M/457.96M | 调用 2348 次

── [10:30:00] +1.2K tokens +3 调用 ──
  deepseek-v4-pro | +1K入/4.9M | +200出/1.19M | +1.2K缓/451.87M | +3调用
  ╌╌╌╌╌ 📅 今日 ╌╌╌╌╌
  deepseek-v4-flash | 入 191.65K | 出 999 | 缓 219.9K | 总计/+缓存 192.65K/412.55K | 调用 16
  deepseek-v4-pro   | 入 3.02M   | 出 323.29K | 缓 119.45M | 总计/+缓存 3.34M/122.79M | 调用 624

── [10:30:05] 无新活动 ──

^C
📊 本次监控汇总
  监控时长: 5 分 30 秒 | 采集 66 轮
```

> ⚠️ watch 模式只能看**一个** Agent，不支持 `--all` 或逗号多选。

---

### 六、导出数据

支持三种格式：XLSX（Excel）、CSV、JSON。年度导出会自动按月分列。

**导出某一个 Agent 的数据：**

```bash
# 导出 Claude Code 全部历史（会弹出格式选择和目录选择）
agent-usage-stats -a claude-code -e

# 导出 Claude Code 今天的数据
agent-usage-stats -a claude-code -t -e

# 导出 Claude Code 本月的数据
agent-usage-stats -a claude-code -m -e

# 导出 Claude Code 今年的数据（自动按月拆分，每月一列）
agent-usage-stats -a claude-code --year -e

# 直接指定导出目录，跳过目录选择（会弹出格式选择）
agent-usage-stats -a claude-code -m -e ~/Desktop
```

**导出所有 Agent 的数据：**

```bash
# 所有 Agent 本月的数据
agent-usage-stats --all -m -e

# 所有 Agent 今年的数据（按月拆分，一张表包含所有 Agent）
agent-usage-stats --all --year -e
```

**选择导出格式：**

运行后会提示你选：
```
选择导出格式:
  [1] XLSX（默认）
  [2] CSV
  [3] JSON
请选择 (1/2/3, 回车=1):
```

直接回车默认选择 XLSX。也可通过管道预设：

```bash
# 选 XLSX（回车=1）
echo 1 | agent-usage-stats -a claude-code -m -e ~/Desktop

# 选 CSV
echo 2 | agent-usage-stats -a claude-code -m -e ~/Desktop

# 选 JSON
echo 3 | agent-usage-stats -a claude-code -m -e ~/Desktop
```

---

### 七、交互式菜单

不带任何参数直接运行，弹出菜单选择要查看的 Agent。

```bash
agent-usage-stats
```

```
🔍 选择你要查看的 AI 助手：
────────────────────────────────────────
  [1] Claude Code
  [2] CodeX
  [3] Hermes
  [4] Reasonix
  [5] DeepSeek TUI
  [a] 所有
  [q] 退出
────────────────────────────────────────
请选择：
```

输入数字就能看对应的 Agent。输入 `a` 看所有。

---

---

### 八、工具维护

**查看帮助（所有命令说明）：**

```bash
agent-usage-stats --help
```

**查看当前版本号：**

```bash
agent-usage-stats -v
# 或
agent-usage-stats --version
```

**把 agent-usage-stats 更新到最新版：**

```bash
agent-usage-stats update
```

如果更新后版本号没变，用强制重装：

```bash
clawhub install ai-agent-usage-stats --force
```

**卸载 agent-usage-stats：**

```bash
# 第 1 步：清理全局命令 + PATH
agent-usage-stats --uninstall

# 第 2 步：移除技能文件
clawhub uninstall ai-agent-usage-stats
```

---

### 各 Agent 的数据怎么看

| Agent | 当前快照 | 时间段 |
|-------|---------|--------|
| **Claude Code** | 总计 + 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 同左 |
| **CodeX** | 总计 + 线程数 | 同左 |
| **Hermes** | 上下文占比 + 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 总计 + 会话数 |
| **OpenClaw** | 上下文占比 + 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 总计 + 调用数 |
| **Reasonix** | 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 同左 |
| **DeepSeek TUI** | 总计 + 会话数 + 工具调用 + 费用 | 同左 |

### 数据来源位置（便于排查问题）

| Agent | 数据读哪里 |
|-------|-----------|
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| CodeX | `~/.codex/state_*.sqlite` → threads 表 |
| Hermes | `~/.hermes/state.db` → sessions 表 |
| OpenClaw | `~/.openclaw/agents/main/sessions/` |
| Reasonix | `~/.reasonix/usage.jsonl` |
| DeepSeek TUI | `~/.deepseek/sessions/*.json` |

### Windows + WSL2 用户

Agent 跑在 WSL2 中时，`agent-usage-stats` 在 Windows 侧自动检测并读取数据。即使 Hermes 正在运行（数据库被锁），也会通过 `wsl.exe` 在 WSL 内部读取，输出标注 `(WSL)`。

1. **WSL 发行版需处于运行状态** — 打开一个 WSL 终端即可
2. **用户名无关联** — 自动探测 WSL 内实际用户目录，与 Windows 登录名无关
3. **代理不影响** — VPN/代理只影响 WSL 网络，不影响本地文件访问

### 支持的模型（69 个模型，13 个厂商）

`agent-usage-stats` 自动识别模型并显示正确的上下文窗口大小。未匹配的模型默认 128K。

| 厂商 | 模型 | 上下文 |
|------|------|--------|
| **Anthropic / Claude** | `claude-opus-4-7`, `claude-opus-4-5`, `claude-opus-4`, `claude-sonnet-4-6`, `claude-sonnet-4-5`, `claude-sonnet-4`, `claude-haiku-4-5`, `claude-haiku-3.5`, `claude-3.5-sonnet`, `claude-3.5-haiku`, `claude-3-opus`, `claude-3-sonnet`, `claude-3-haiku` | 200K |
| **OpenAI / GPT** | `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano` | 1M |
| | `gpt-4o`, `gpt-4o-mini`, `gpt-4-turbo`, `gpt-4` | 128K |
| | `o4-mini`, `o3`, `o3-mini`, `o1`, `o1-pro` | 200K |
| **Google / Gemini** | `gemini-2.5-pro`, `gemini-2.5-flash`, `gemini-2.5-flash-lite`, `gemini-2.0-flash` | 1M |
| **DeepSeek** | `deepseek-v4-pro`, `deepseek-v4-flash`, `deepseek-v4`, `deepseek-chat`, `deepseek-reasoner`, `deepseek-r1` | 1M |
| | `deepseek-v3` | 128K |
| **通义千问 / Qwen** | `qwen3`, `qwen3-coder`, `qwen2.5-coder`, `qwen-plus`, `qwen-max`, `qwen-turbo` | 128K |
| **Kimi / 月之暗面** | `moonshot-v1-128k`, `moonshot-v1-32k`, `moonshot-v1-8k`, `kimi-latest` | 8K~128K |
| **GLM / 智谱** | `glm-4-plus`, `glm-4-long` (1M), `glm-4-air`, `glm-4-flash`, `glm-4`, `glm-3-turbo` | 128K~1M |
| **Doubao / 字节豆包** | `doubao-pro-128k`, `doubao-pro-32k`, `doubao-lite-32k` | 32K~128K |
| **文心 / 百度** | `ernie-4.0-turbo`, `ernie-4.0`, `ernie-3.5` | 8K~128K |
| **Meta / Llama** | `llama-4`, `llama-3.1`, `llama-3` | 128K |
| **Mistral** | `mistral-large-2`, `mistral-large`, `mistral-small` | 128K |
| **xAI / Grok** | `grok-3`, `grok-2` | 128K |
| **零一万物 / Yi** | `yi-large`, `yi-lightning` | 16K~32K |

前缀匹配支持: `claude-opus-4-7-20250219` → 200K, `gpt-4.1-preview` → 1M, `deepseek-v4-0324` → 1M。

---

## 卸载

```bash
# 第 1 步：清理全局命令 + PATH（自动）
agent-usage-stats --uninstall

# 第 2 步：移除技能文件
clawhub uninstall ai-agent-usage-stats
```

> `--uninstall` 会自动删除包装器、清理 PATH 条目、删除配置文件。三平台统一。

---

## 兼容性

| 平台 | 状态 |
|------|------|
| macOS | ✅ 完整支持 |
| Linux | ✅ 完整支持 |
| Windows | ✅ 支持（`.cmd` 包装器） |

| 环境 | 要求 |
|------|------|
| Python | 3.11+（标准库，零 pip 依赖） |
| Node.js | 仅安装时需要（装 ClawHub） |

---

## 常见问题与排查指南

### 安装问题

#### ❓ `clawhub install ai-agent-usage-stats` 报错

**可能原因：网络问题或 Node.js 版本过旧。**

```bash
# 检查 Node.js 版本（需要 v18+）
node --version

# 重装 ClawHub
npm install -g clawhub

# 如果在国内网络慢，可尝试
npm install -g clawhub --registry=https://registry.npmmirror.com
```

<a id="setup-not-found"></a>
#### ❓ 安装文件路径异常排查

**适用场景：执行 `setup` 时提示文件不存在。**

**原因：没有先 `cd ~` 再执行 `clawhub install`**，技能被装到了其他目录。

**解决：**
```bash
cd ~
clawhub install ai-agent-usage-stats --force
```

然后按上方安装指引执行 `setup`。主目录 (`~`) 在所有系统上都有写入权限，不会出现权限问题。

<a id="ps-tilde"></a>
#### ❓ PowerShell 报 `can't open file '...~...'`

**原因：PowerShell 作为命令行参数传递 `~` 时不会展开**，`~` 被当作字面量目录名。

错误示例：
```
python: can't open file 'C:\\Users\\xxx\\~\\skills\\...': No such file or directory
```

**解决：用 `$HOME` 替代 `~`：**
```powershell
# ❌ 错误
python ~\skills\ai-agent-usage-stats\agent-usage-stats.py setup

# ✅ 正确
python $HOME\skills\ai-agent-usage-stats\agent-usage-stats.py setup
```

> `$HOME` 是 PowerShell 内置变量，始终展开为当前用户目录。

#### ❓ `agent-usage-stats` 命令找不到

**原因 1：还没执行 `setup`** → 按上方安装指引执行 `python $HOME\skills\...\agent-usage-stats.py setup`（Windows）或 `python3 ~/skills/.../agent-usage-stats.py setup`（macOS/Linux）。

**原因 2：执行了 `setup` 但没新开终端** → `setup` 已将 PATH 写入系统配置，但当前终端不生效，新开一个终端即可。

**原因 3：setup 执行失败** → 重新执行 `setup`，观察是否有报错。如果 PATH 添加失败，可手动添加：

**macOS（zsh）：**
```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.zshrc
source ~/.zshrc
```

**Linux（bash）：**
```bash
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
source ~/.bashrc
```

**Windows（PowerShell 临时）：**
```powershell
$env:PATH += ';' + "$env:USERPROFILE\.local\bin"
```

#### ❓ 执行 `agent-usage-stats` 报 `Permission denied`

**仅 macOS / Linux。原因：包装器脚本没有执行权限。**

```bash
chmod +x ~/.local/bin/agent-usage-stats
# 或者重新执行 setup
python3 ~/skills/ai-agent-usage-stats/agent-usage-stats.py setup
```

> Windows 用户不受此问题影响（`.cmd` 文件不需要执行权限）。

### 运行问题

#### ❓ 菜单里看不到我装的 Agent

**原因：`agent-usage-stats` 通过检查特定路径来判断 Agent 是否已安装。** 这些路径存在才会显示：

| Agent | 检测路径 |
|-------|---------|
| **Claude Code** | `~/.claude/projects/` |
| **CodeX** | `~/.codex/state_*.sqlite` |
| **Hermes** | `~/.hermes/state.db` |
| **OpenClaw** | `~/.openclaw/agents/main/sessions/sessions.json` |
| **Reasonix** | `~/.reasonix/usage.jsonl` |
| **DeepSeek TUI** | `~/.deepseek/sessions/` |

可以先用 `agent-usage-stats --list-backends` 看具体哪个被检测到了。

#### ❓ 统计显示「无数据」或数字为 0

**可能原因：**

1. **Agent 虽然装了但还没使用过** → 先去用一下再回来查
2. **数据文件路径不对** → 运行 `agent-usage-stats --list-backends` 确认是否被检测到
3. **时间段内没有数据** → 如果是 `--today` 或 `--from 2026-01-01`，确认该时间段内确实有会话

#### ❓ 对比结果显示 `unknown` 模型

**Hermes 数据库中部分会话的 model 字段为空**，不影响正常统计。可以用这个命令排查：

```bash
sqlite3 ~/.hermes/state.db "SELECT DISTINCT model FROM sessions WHERE model IS NULL OR model = ''"
```

> Windows 用户如果没有 `sqlite3` 命令，可以用 Python 替代：
> ```powershell
> python3 -c "import sqlite3; c=sqlite3.connect(r'$env:USERPROFILE\.hermes\state.db'); print('\n'.join(r[0] or '(NULL)' for r in c.execute('SELECT DISTINCT model FROM sessions WHERE model IS NULL OR model = \"\"')))"
> ```
