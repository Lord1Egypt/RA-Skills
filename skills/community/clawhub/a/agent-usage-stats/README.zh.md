# token-stats — AI Agent Token 消耗统计工具

统计当前设备上 AI 编程助手的 token 消耗，支持多 Agent、多模型、多时间段查询与导出。

## 为什么选择 token-stats

`token-stats` 直接读取本地数据，跨 Agent、跨模型、跨平台运行。零依赖，纯 Python 标准库。

| 功能 | 命令 | 说明 |
|------|------|------|
| **Token 消耗统计** — 指定时间范围 | `token-stats -a claude-code --month` | 多 Agent（Claude Code / CodeX / Hermes / OpenClaw / Reasonix / DeepSeek TUI）、多模型，输入/输出/缓存 token 和调用次数，有数据才展示 |
| **实时监控** — Token 增量追踪 | `token-stats -a claude-code --watch` | 每轮增量 + 累计量 + 停止后汇总，macOS / Linux / Windows 通用 |
| **时段对比** — 两个时间段并排比较 | `--compare --a yesterday --b today` | 任意时间段聚合，多模型横向对比，带差值列 |
| **数据导出** — XLSX / CSV / JSON | `--export` | 多 Agent、多时间段组合，交互式选目录；年度按月拆分 |
| **本地账本** — 汇总用量展示 | `token-stats --all --month` | 只读本机 SQLite / JSONL，用汇总数据看输入、输出、缓存、调用和成本 |

---

## 环境要求

安装前需满足以下环境要求：

### 1. Python 3.11+

`token-stats` 本身是纯 Python 脚本，依赖标准库，不需要额外 pip 装任何包。

```bash
# 检查已安装（Windows 用户用 python --version）
python3 --version

# 如未安装 → https://www.python.org/downloads/
```

### 2. Node.js（安装工具时需要）

`token-stats` 通过 **ClawHub CLI** 安装。ClawHub 是个 Node.js 命令行工具。

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

> ⚠️ `token-stats` **仅统计当前设备的数据，不跨机器汇总**。
>
> - **同一把 API Key 用在多台机器 → 每台机器的统计互不相通**
> - 例：API Key 同时在 PC A 和 PC B 用，PC A 的 `token-stats` 只看得到 PC A 的用量
> - `token-stats` 不联网、不查 API 后台，纯读当前设备上的数据文件
> - 要看另一台机器的统计，请在那台机器上也安装 `token-stats`
>
> 🕐 **时区说明**：`--today` / `--yesterday` 等时间段基于**系统时区**。例如北京时间 (UTC+8) 的 `--today` 统计范围为当日 00:00~23:59 CST。跨时区机器看到的数据范围不同。

### API 中转站

通过中转站访问大模型时，统计准确性取决于中转站是否**原样透传** API 返回的 `usage` 字段。`token-stats` 只记录 Agent 本地写入的数据，不校验与上游 API 是否一致。

### 统计原理

`token-stats` 读取各 Agent 写入本地的数据文件（SQLite / JSONL），按模型聚合 `usage` 对象中的 `input_tokens`、`output_tokens`、`cache_read_tokens` 和调用次数。数据链路：

```
API 返回 usage → Agent 写入本地 → token-stats 读取汇总
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

**token-stats 计算方式**：各 Agent 底层 API 不同，采用自适应公式：

```
如果 cache > input:  缓存率 = cache / (cache + input)   ← DeepSeek API（input = cache_miss）
如果 cache ≤ input:  缓存率 = cache / input              ← 标准 API（input = 总 prompt）
```

| Agent | 数据来源 | 精确度 |
|-------|---------|:---:|
| Reasonix | `cacheHitTokens` + `cacheMissTokens` 均已知 | 精确 |
| Claude Code / Hermes / OpenClaw | `cache_read_input_tokens`（无 creation） | 近似(偏保守) |
| CodeX / DeepSeek TUI | 有缓存数据（CodeX 从 session JSONL 读取） | 精确/无数据 |

- `cache = 0` 时不展示缓存率
- 对于 Anthropic API，`input_tokens` 包含不参与缓存的 tokens，实际命中率略高于展示值
- 监控模式增量段的缓存率表示该时间窗口内的命中比例

## 安装

通过 **ClawHub** 安装。安装后再执行一次 `setup`，它会把运行文件复制到 `~/.token-stats/`，创建 `~/.token-stats/bin/token-stats`，并将 `~/.token-stats/bin` 加入 PATH。

**macOS / Linux：**
```bash
cd ~
clawhub install agent-usage-stats
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

**Windows（PowerShell）：**
```powershell
cd $HOME
clawhub install agent-usage-stats
python $HOME\skills\agent-usage-stats\token-stats.py setup
```

更新：

```bash
token-stats update
# 或者先更新 ClawHub 技能，再重新 setup
clawhub update agent-usage-stats
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

卸载：

```bash
token-stats --uninstall
```

如需同时移除 ClawHub 下载的技能目录，可删除 `~/skills/agent-usage-stats/`。

安装完成后，新开终端即可使用 `token-stats` 命令。

### 更新

```bash
token-stats update
```
> 内部调用 `clawhub update agent-usage-stats`，拉取新版本后复制到 `~/.token-stats/`。

### 验证安装成功

```bash
# 验证 1：版本号
token-stats --version
# 输出: token-stats v2.7.13

# 验证 2：看已检测到的 Agent
token-stats --list-backends
# 输出示例:
#   ✅ Claude Code
#   ✅ CodeX
#   ✅ Hermes
#   ❌ OpenClaw
#   ✅ Reasonix
#   ✅ DeepSeek TUI

# 验证 3：直接看某个 Agent 的统计
token-stats -a claude-code --month
# 输出示例:
# 📊 Claude Code
#   deepseek-v4-flash | 入 6.44M  | 出 320.28K | 缓 27.86M (81.2%)   | 总计/+缓存 6.76M/34.62M    | 调用 1313 次
#   deepseek-v4-pro   | 入 13.12M | 出 6.36M   | 缓 2471.2M (99.5%)  | 总计/+缓存 19.47M/2490.67M | 调用 11835 次
#   合计              | 入 19.66M | 出 6.68M   | 缓 2499.06M (99.2%) | 总计/+缓存 26.34M/2525.4M  | 调用 13153 次
```

以上三条均正常输出即表示安装成功。

## 更新

通过 ClawHub 更新到最新版本：

```bash
token-stats update
# 或
clawhub update agent-usage-stats
```

> `update` 原地替换文件，包装器和 PATH 均无需重配。

> 💡 更新后版本没变？加 `--force` 强制拉取：
> ```
> clawhub install agent-usage-stats --force
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

示例：`token-stats -a claude-code --today`

### 快速参考

| 操作 | 命令 | 适用范围 |
|------|------|---------|
| 查看今日所有 Agent 统计 | `token-stats --all -t` | 所有 Agent |
| 查看本月统计 | `token-stats --all -m` | 所有 Agent |
| 查看单个 Agent | `token-stats -a claude-code` | 单个 Agent |
| 当前快照/详细模式 | `token-stats -a claude-code --now` / `--detail` | 单个 Agent |
| 实时监控 | `token-stats -a claude-code -w` | 单个 Agent |
| 时段对比 | `token-stats -a claude-code --compare --a last-week --b this-week` | 单个 Agent |
| 导出数据 | `token-stats -a claude-code -m -e` | 单个/所有 Agent |
| 列出已安装 Agent | `token-stats --list-backends` | 当前设备检测 |
| 更新/卸载 | `token-stats update` / `token-stats --uninstall` | 工具维护 |
| 交互式菜单 | `token-stats` | 交互式选择 |

### 参数说明

| 短参数 | 长参数 | 说明 |
|:---:|---|---|
| `-a` | `--agent` | 指定 Agent，名称见上方 Agent 名称表。多个用逗号分隔 |
| `-t` | `--today` | 今日数据 |
| | `--yesterday` | 昨日数据 |
| | `--week` | 本周数据（周一至今） |
| | `--last-7d` | 最近 7 天数据 |
| `-m` | `--month` | 本月数据（1 号至今） |
| `-y` | `--year` | 今年数据（1 月 1 日至今） |
| | `--from` / `--to` | 自定义日期范围，格式 `YYYY-MM-DD` |
| `-w` | `--watch` | 实时监控，默认 5 秒刷新，Ctrl+C 停止 |
| `-e` | `--export` | 导出为 XLSX / CSV / JSON |
| `-v` | `--version` | 查看版本号 |
| `-l` | `--list-backends` | 列出当前设备已检测到的 Agent |
| | `--compare` / `--a` / `--b` | 对比两个时间段 |
| | `--now` / `--detail` | 当前快照/详细模式（等同默认统计） |
| `--all` | | 查看所有 Agent 统计 |
| | `setup` / `--setup` | 安装到 `~/.token-stats/`，创建 `~/.token-stats/bin/token-stats` 并加入 PATH |
| | `update` / `--update` | 更新到最新版 |
| | `--uninstall` | 删除全局命令、安装目录并清理 PATH |

> 短参数可组合使用。例如 `-a claude-code -t -e` 表示导出 Claude Code 今日数据。
> README 中的输出为脱敏示例；实际数字会因 Agent、模型、时区和使用量不同而不同。

---

### 一、查看单个 Agent

以下示例以 Claude Code 为例，可替换为其他 Agent（`codex` / `hermes` / `openclaw` / `reasonix` / `deepseek-tui`）。

**直接看全部历史（不限时间段）：**

```bash
token-stats -a claude-code
```

输出形态：

```
📊 Claude Code
  deepseek-v4-flash | 入 439.99K | 出 21.11K  | 缓 1.81M (80.5%)  | 总计/+缓存 461.1K/2.27M   | 调用 60 次  | ≈¥0.52
  deepseek-v4-pro   | 入 733.74K | 出 122.12K | 缓 24.45M (97.1%) | 总计/+缓存 855.86K/25.31M | 调用 176 次 | ≈¥3.55
  合计              | 入 1.17M   | 出 143.23K | 缓 26.26M (95.7%) | 总计/+缓存 1.32M/27.58M   | 调用 236 次 | ≈¥4.06 (仅供参考)
```

**当前快照/详细模式（等同默认统计）：**

```bash
token-stats -a claude-code --now
token-stats -a claude-code --detail
```

输出同默认统计，用于明确表达“查看当前快照”：

```
📊 Claude Code
  deepseek-v4-pro | 入 13.12M | 出 6.36M | 缓 2471.2M (99.5%) | 总计/+缓存 19.47M/2490.67M | 调用 11835 次
  合计            | 入 19.66M | 出 6.68M | 缓 2499.06M (99.2%) | 总计/+缓存 26.34M/2525.4M  | 调用 13153 次
```

**只看今天的：**

```bash
token-stats -a claude-code -t
```

输出形态：

```
Claude Code: 会话文件中未解析到有效数据
```

当天没有记录时会显示无有效数据；有记录时输出表格结构与本月示例相同。

**看昨天的：**

```bash
token-stats -a claude-code --yesterday
```

输出形态：

```
📊 Claude Code
```

某些时间段没有有效记录时，仅显示标题或无数据提示。

**看本月的（1 号到今天）：**

```bash
token-stats -a claude-code -m
```

**看今年的（1 月 1 号到今天）：**

```bash
token-stats -a claude-code --year
```

输出形态：

```
📊 Claude Code
  Qwen3-Coder-30B-A3B-Instruct-MLX-4bit | 入 22.91K | 出 131   | 缓 0                | 总计/+缓存 23.04K/23.04K   | 调用 1 次
  deepseek-v4-flash                     | 入 6.44M  | 出 320K  | 缓 27.86M (81.2%)   | 总计/+缓存 6.76M/34.62M    | 调用 1313 次
  deepseek-v4-pro                       | 入 13.12M | 出 6.36M | 缓 2471.2M (99.5%)  | 总计/+缓存 19.47M/2490.67M | 调用 11835 次
  合计                                  | 入 19.66M | 出 6.68M | 缓 2499.06M (99.2%) | 总计/+缓存 26.34M/2525.4M  | 调用 13153 次
```

**看本周的（周一到今天）：**

```bash
token-stats -a claude-code --week
```

输出形态：

```
📊 Claude Code
```

**看最近 7 天的：**

```bash
token-stats -a claude-code --last-7d
```

输出形态：

```
📊 Claude Code
  deepseek-v4-flash | 入 4.42M  | 出 242.8K | 缓 19.5M (81.5%)    | 总计/+缓存 4.66M/24.16M    | 调用 964 次
  deepseek-v4-pro   | 入 8.12M  | 出 5.07M  | 缓 1944.99M (99.6%) | 总计/+缓存 13.2M/1958.19M  | 调用 9249 次
  合计              | 入 12.54M | 出 5.31M  | 缓 1964.49M (99.4%) | 总计/+缓存 17.85M/1982.35M | 调用 10213 次
```

**自己指定日期范围：**

```bash
# 从 5 月 1 号到 5 月 28 号
token-stats -a claude-code --from 2026-05-01 --to 2026-05-28
```

输出示例：

```
📊 Claude Code
  Qwen3-Coder-30B-A3B-Instruct-MLX-4bit | 入 22.91K | 出 131     | 缓 0                | 总计/+缓存 23.04K/23.04K   | 调用 1 次     | -
  deepseek-v4-flash                     | 入 6.44M  | 出 320.28K | 缓 27.86M (81.2%)   | 总计/+缓存 6.76M/34.62M    | 调用 1313 次  | ≈¥7.63
  deepseek-v4-pro                       | 入 13.12M | 出 6.36M   | 缓 2471.2M (99.5%)  | 总计/+缓存 19.47M/2490.67M | 调用 11835 次 | ≈¥139.26
  gemma-4-26B-A4B-it-MLX-4bit           | 入 89.18K | 出 1.08K   | 缓 0                | 总计/+缓存 90.26K/90.26K   | 调用 4 次     | -
  合计                                  | 入 19.66M | 出 6.68M   | 缓 2499.06M (99.2%) | 总计/+缓存 26.34M/2525.4M  | 调用 13153 次 | ≈¥146.89 (仅供参考)
  ────────────────────────────────────
  子代理: 89 次 | 会话: 65 个 | 项目: 5 个
```

---

### 二、查看多个 Agent

**指定 Agent 列表（逗号分隔）：**

```bash
# 同时看 Hermes 和 Claude Code 本月的数据
token-stats -a hermes,claude-code -m
```

输出形态：

```
📊 Hermes
  deepseek-v4-flash | 入 2.03M | 出 819.69K | 缓 223.53M (99.1%) | 总计/+缓存 2.85M/226.39M | 调用 2075 次

📊 Claude Code
  deepseek-v4-pro | 入 733.74K | 出 122.12K | 缓 24.45M (97.1%) | 总计/+缓存 855.86K/25.31M | 调用 176 次

全部 Agent 总计
  入 2.76M | 出 941.81K | 缓 247.98M (98.9%) | 总计/+缓存 3.7M/251.68M | 调用 2251 次
```

**一次性看电脑上所有 Agent 的数据：**

```bash
# 全部历史（不限时间段）
token-stats --all

# 所有 Agent 今天的数据
token-stats --all -t

# 所有 Agent 本月的数据
token-stats --all -m

# 所有 Agent 今年的数据
token-stats --all --year
```

输出示例：

```
📊 本机 Agent 统计汇总
══════════════════════════════════════════════════

✅ Claude Code
📊 Claude Code
  deepseek-v4-flash | 入 6.44M  | 出 320.28K | 缓 27.86M (81.2%)   | 总计/+缓存 6.76M/34.62M    | 调用 1313 次  | ≈¥7.63
  deepseek-v4-pro   | 入 13.12M | 出 6.36M   | 缓 2471.2M (99.5%)  | 总计/+缓存 19.47M/2490.67M | 调用 11835 次 | ≈¥139.26
  合计              | 入 19.66M | 出 6.68M   | 缓 2499.06M (99.2%) | 总计/+缓存 26.34M/2525.4M  | 调用 13153 次 | ≈¥146.89 (仅供参考)

✅ CodeX
📊 CodeX
  gpt-5.5           | 入 7.54M   | 出 633.52K | 缓 99.93M (93.0%) | 总计/+缓存 8.17M/108.11M | 调用 1082 次 | ≈¥2222.39
  codex-auto-review | 入 129.86K | 出 3.2K    | 缓 915.58K (87.6%) | 总计/+缓存 133.06K/1.05M | 调用 23 次   | ≈¥0.00
  deepseek-v4-flash | 入 16.32K  | 出 816     | 缓 63.87K (79.6%)  | 总计/+缓存 17.14K/81.01K | 调用 6 次    | ≈¥0.02
  合计              | 入 7.69M   | 出 637.54K | 缓 100.91M (92.9%) | 总计/+缓存 8.32M/109.23M | 调用 1111 次 | ≈¥2222.41 (仅供参考)

✅ Hermes
Hermes: 该时间段内无会话记录

✅ Reasonix
📊 Reasonix
Reasonix: usage.jsonl 中无有效数据

✅ DeepSeek TUI
📊 DeepSeek TUI
DeepSeek TUI: 尚无会话记录

══════════════════════════════════════════════════
  全部 Agent 总计
  入 8.86M | 出 780.77K | 缓 127.17M (93.5%) | 总计/+缓存 9.64M/136.82M | 调用 1347 次 | ≈¥2226.47 (仅供参考)
```

---

### 三、列出已安装的 Agent

```bash
# 短参数
token-stats -l

# 长参数
token-stats --list-backends
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
token-stats -a claude-code --compare --a yesterday --b today
```

输出形态：

```
📊 对比: 2026-05-28 vs 2026-05-29  [Claude Code]
  两个时间段均无数据
```

**上周和这周比：**

```bash
token-stats -a claude-code --compare --a last-week --b this-week
```

**上个月和这个月比：**

```bash
token-stats -a claude-code --compare --a last-month --b this-month
```

**去年和今年比：**

```bash
token-stats -a claude-code --compare --a last-year --b this-year
```

输出形态：

```
📊 对比: 2025-01-01~2025-12-31 vs 2026-01-01~2026-12-31  [Claude Code]
  deepseek-v4-pro | 总计         | 0 | 19471960   | +19.47M
                  | 调用         | 0 | 11835      | +11.84K
  合计            | 总计(含缓存) | 0 | 2525403348 | +2525.4M
```

**两个自定义日期比：**

```bash
# 两个具体的某一天
token-stats -a claude-code --compare --a 2026-01-01 --b 2026-01-15

# 两个日期范围（用 ~ 连接）
token-stats -a claude-code --compare --a 2026-01-01~2026-01-07 --b 2026-01-08~2026-01-14
```

支持的标签：`today` / `yesterday` / `this-week` / `last-week` / `this-month` / `last-month` / `this-year` / `last-year` / `YYYY-MM-DD` / `YYYY-MM-DD~YYYY-MM-DD`

输出示例（`token-stats -a codex --compare --a last-week --b this-week`）：

```
📊 对比: 2026-05-25~2026-05-31 vs 2026-06-01~2026-06-07  [CodeX]
===============================================================================================
  模型   | 指标         | 2026-05-25~2026-05-31 | 2026-06-01~2026-06-07 | 变化
───────────────────────────────────────────────────────────────────────────────────────────────
  gpt-5.5 | 总计         | 5.3M                  | 8.18M                 | +2.88M
         | 总计(含缓存) | 69.63M                | 108.18M               | +38.55M
         | 调用         | 878                   | 1083                  | +205
         | 费用         | ≈¥1438.90             | ≈¥2223.81             | +¥784.91
  合计   | 入           | 4.93M                 | 7.69M                 | +2.76M
         | 出           | 447.74K               | 637.77K               | +190.03K
         | 缓           | 64.56M                | 100.98M               | +36.42M
         | 总计         | 5.38M                 | 8.33M                 | +2.95M
         | 调用         | 888                   | 1112                  | +224
         | 费用         | ≈¥1438.90             | ≈¥2223.83             | +¥784.93
───────────────────────────────────────────────────────────────────────────────────────────────
```

---

### 五、实时监控

按指定间隔刷新 token 消耗数据，支持增量展示和今日累计。Ctrl+C 停止后显示本次监控汇总。

**默认 5 秒刷新一次：**

```bash
token-stats -a claude-code -w
```

**自定义刷新间隔（比如 2 秒一次）：**

```bash
token-stats -a claude-code -w 2
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
token-stats -a claude-code -e

# 导出 Claude Code 今天的数据
token-stats -a claude-code -t -e

# 导出 Claude Code 本月的数据
token-stats -a claude-code -m -e

# 导出 Claude Code 今年的数据（自动按月拆分，每月一列）
token-stats -a claude-code --year -e

# 直接指定导出目录，跳过目录选择（会弹出格式选择）
token-stats -a claude-code -m -e ~/Desktop
```

**导出所有 Agent 的数据：**

```bash
# 所有 Agent 本月的数据
token-stats --all -m -e

# 所有 Agent 今年的数据（按月拆分，一张表包含所有 Agent）
token-stats --all --year -e
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
echo 1 | token-stats -a claude-code -m -e ~/Desktop

# 选 CSV
echo 2 | token-stats -a claude-code -m -e ~/Desktop

# 选 JSON
echo 3 | token-stats -a claude-code -m -e ~/Desktop
```

---

输出形态：

```
选择导出格式:
  [1] XLSX（默认）
  [2] CSV
  [3] JSON
请选择 (1/2/3, 回车=1): ✅ 已导出到: /path/to/token-stats_claude-code_20260529_001709.csv
```

### 七、交互式菜单

不带任何参数直接运行，弹出菜单选择要查看的 Agent。

```bash
token-stats
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
token-stats --help
```

输出形态：

```
usage: token-stats.py [-h] [-v] [-l] [-a AGENT] [-w [秒]] [-t] [--yesterday] ...

命令大全:
  基础:
    token-stats                       交互式菜单选择 Agent → 查看统计
    token-stats -a <name>             直接指定 Agent
  快速时间段:
    token-stats -a <name> -t / --today
    token-stats -a <name> -m / --month
  对比:
    token-stats -a <name> --compare --a today --b yesterday
```

**查看当前版本号：**

```bash
token-stats -v
# 或
token-stats --version
```

输出：

```
token-stats v2.7.13
```

**把 token-stats 更新到最新版：**

```bash
token-stats update
```

输出形态：

```
🔄 正在通过 ClawHub 更新 agent-usage-stats...
✅ 已更新 token-stats 到: ~/.token-stats
```

如果更新后版本号没变，用强制重装：

```bash
clawhub install agent-usage-stats --force
```

**卸载 token-stats：**

```bash
token-stats --uninstall
```

输出形态：

```
🗑️ 正在卸载 token-stats...
✅ 已删除全局命令
✅ 已删除安装目录
✅ 卸载完成
```

**ClawHub 安装后执行 setup：**

```bash
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

输出形态：

```
✅ 已安装 token-stats 到: ~/.token-stats
✅ 已创建全局命令: ~/.token-stats/bin/token-stats
```

---

### 各 Agent 的数据怎么看

| Agent | 当前快照 | 时间段 |
|-------|---------|--------|
| **Claude Code** | 总计 + 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 同左 |
| **CodeX** | 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 同左 |
| **Hermes** | 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 + 会话数 | 总计 + 会话数 |
| **OpenClaw** | 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 总计 + 调用数 |
| **Reasonix** | 输入/输出/缓存 + 调用次数 + 缓存率 + 预估费用 | 同左 |
| **DeepSeek TUI** | 总计 + 会话数 + 工具调用 + 预估费用 | 同左 |

> **说明**：DeepSeek TUI 展示的「工具调用」与其他 Agent 的「调用」含义不同。其他 Agent 的「调用」指 API 请求次数，而 DeepSeek TUI 统计的是会话中模型实际执行工具（读文件、搜索、执行命令等）的次数。这是由 DeepSeek TUI 的 session 数据模型决定的。

### 数据来源位置（便于排查问题）

| Agent | 数据读哪里 |
|-------|-----------|
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| CodeX | `~/.codex/state_*.sqlite` → threads 表 + `~/.codex/sessions/**/*.jsonl` → token_count 事件 |
| Hermes | `~/.hermes/state.db` → sessions 表 |
| OpenClaw | `~/.openclaw/agents/main/sessions/` |
| Reasonix | `~/.reasonix/usage.jsonl` |
| DeepSeek TUI | `~/.deepseek/sessions/*.json` |

### Windows + WSL2 用户

Agent 跑在 WSL2 中时，`token-stats` 在 Windows 侧自动检测并读取数据。即使 Hermes 正在运行（数据库被锁），也会通过 `wsl.exe` 在 WSL 内部读取，输出标注 `(WSL)`。

1. **WSL 发行版需处于运行状态** — 打开一个 WSL 终端即可
2. **用户名无关联** — 自动探测 WSL 内实际用户目录，与 Windows 登录名无关
3. **代理不影响** — VPN/代理只影响 WSL 网络，不影响本地文件访问

### 模型名称处理

`token-stats` 按 Agent 本地记录里的模型名称聚合用量。已配置的名称可参与费用估算；未匹配的名称仍会正常出现在汇总里，只是不参与预估费用。

---

## 卸载

```bash
# 第 1 步：清理全局命令 + PATH（自动）
token-stats --uninstall
```

> `--uninstall` 会自动删除包装器、清理 PATH 条目、删除配置文件、删除 `~/.token-stats/`，并清理 `~/skills/agent-usage-stats` 等 ClawHub/历史安装目录，保证后续可以干净重装。三平台统一。

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

#### ❓ `clawhub install agent-usage-stats` 报错

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
clawhub install agent-usage-stats --force
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
python ~\skills\agent-usage-stats\token-stats.py setup

# ✅ 正确
python $HOME\skills\agent-usage-stats\token-stats.py setup
```

> `$HOME` 是 PowerShell 内置变量，始终展开为当前用户目录。

#### ❓ `token-stats` 命令找不到

**原因 1：还没执行 `setup`** → 按上方 ClawHub 安装指引执行 setup。

**原因 2：执行了 `setup` 但没新开终端** → `setup` 已将 PATH 写入系统配置，但当前终端不生效，新开一个终端即可。

**原因 3：setup 执行失败** → 重新执行 `setup`，观察是否有报错。如果 PATH 添加失败，可手动添加：

**macOS（zsh）：**
```bash
echo 'export PATH="$HOME/.token-stats/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux（bash）：**
```bash
echo 'export PATH="$HOME/.token-stats/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Windows（PowerShell 临时）：**
```powershell
$env:PATH += ';' + "$env:USERPROFILE\.token-stats\bin"
```

#### ❓ 执行 `token-stats` 报 `Permission denied`

**仅 macOS / Linux。原因：包装器脚本没有执行权限。**

```bash
chmod +x ~/.token-stats/bin/token-stats
# 或者重新执行 setup
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

> Windows 用户不受此问题影响（`.cmd` 文件不需要执行权限）。

### 运行问题

#### ❓ 菜单里看不到我装的 Agent

**原因：`token-stats` 通过检查特定路径来判断 Agent 是否已安装。** 这些路径存在才会显示：

| Agent | 检测路径 |
|-------|---------|
| **Claude Code** | `~/.claude/projects/` |
| **CodeX** | `~/.codex/state_*.sqlite` |
| **Hermes** | `~/.hermes/state.db` |
| **OpenClaw** | `~/.openclaw/agents/main/sessions/sessions.json` |
| **Reasonix** | `~/.reasonix/usage.jsonl` |
| **DeepSeek TUI** | `~/.deepseek/sessions/` |

可以先用 `token-stats --list-backends` 看具体哪个被检测到了。

#### ❓ 统计显示「无数据」或数字为 0

**可能原因：**

1. **Agent 虽然装了但还没使用过** → 先去用一下再回来查
2. **数据文件路径不对** → 运行 `token-stats --list-backends` 确认是否被检测到
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
