# token-stats — Pick an Agent, See Its Token Burn

Run it, pick an agent, see the stats. Every time.

## What's this?

You have multiple AI assistants on one device (Hermes, Claude Code, CodeX, OpenClaw, Reasonix, DeepSeek TUI…).
`token-stats` lets you **choose one and see how many tokens it's consuming**.

> ⚠️ **Important: this tool only reads local agent data on the current device.**
> If you run agents on different PCs or servers, each device stores its own data
> and needs its own installation of `token-stats`. Cross-machine statistics are not supported.
>
> All statistics are queried based on the specific agent you select, not a global total.

---

## Why token-stats

`token-stats` reads local data directly — works across agents, models, and platforms. Zero dependencies, pure Python stdlib.

| Feature | Command | Description |
|---------|---------|-------------|
| **Token stats** — by time range | `token-stats -a hermes --month` | Multi-agent (Hermes / Claude Code / CodeX / OpenClaw / Reasonix / DeepSeek TUI), multi-model. Input/output/cache tokens + call counts, only models with data |
| **Live monitor** — token delta tracking | `token-stats -a hermes --watch` | Per-round delta + cumulative summary. macOS / Linux / Windows |
| **Compare** — side-by-side periods | `--compare --a yesterday --b today` | Any time range, multi-model comparison with diff column |
| **Export** — XLSX / CSV / JSON | `--export` | Multi-agent, multi-period combinations. Interactive directory picker |
| **Local ledger** — usage summaries | `token-stats --all --month` | Reads local SQLite / JSONL only; summarizes input/output/cache tokens, calls, and cost |

---

## Environment Requirements

Before installing `token-stats`, make sure you have these:

### 1. Python 3.11+

`token-stats` is a pure Python script using only stdlib — no pip packages needed.

```bash
# Check (Windows users: use python --version)
python3 --version

# If missing → https://www.python.org/downloads/
```

### 2. Node.js (needed for the installer)

`token-stats` is distributed via **ClawHub CLI**, a Node.js command-line tool.

```bash
# Check
node --version

# If missing → https://nodejs.org (get the LTS version)
```

Node.js includes `npm`, which is used to install ClawHub.

### 3. ClawHub CLI

```bash
# Install
npm install -g clawhub

# Verify
clawhub -V          # show version
```

> 💡 On macOS with Homebrew-installed Node.js, `npm install -g clawhub` puts it at `/opt/homebrew/bin/clawhub`, which is usually already in your PATH.

> 💡 If you're in China and npm is slow, use the npmmirror registry:
> ```bash
> npm install -g clawhub --registry=https://registry.npmmirror.com
> ```

---

## Install

Install with **ClawHub**. After ClawHub downloads the skill, run `setup`; it copies the runtime files into `~/.token-stats/`, creates `~/.token-stats/bin/token-stats`, and adds `~/.token-stats/bin` to PATH.

**macOS / Linux:**
```bash
cd ~
clawhub install agent-usage-stats
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

**Windows (PowerShell):**
```powershell
cd $HOME
clawhub install agent-usage-stats
python $HOME\skills\agent-usage-stats\token-stats.py setup
```

Update:

```bash
token-stats update
# Or update the ClawHub skill first, then run setup again
clawhub update agent-usage-stats
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

Uninstall:

```bash
token-stats --uninstall
```

To also remove the ClawHub-downloaded files, delete `~/skills/agent-usage-stats/`.

That's it. Open a new terminal and run `token-stats`.

### Update

```bash
token-stats update
```
> This runs `clawhub update agent-usage-stats` internally, then copies updated files into `~/.token-stats/`.

### Verify Installation

```bash
# Check 1: version
token-stats --version
# Output: token-stats v2.7.13

# Check 2: list installed agents
token-stats --list-backends
# Example output:
#   ✅ Claude Code
#   ✅ CodeX
#   ✅ Hermes
#   ❌ OpenClaw
#   ✅ Reasonix
#   ✅ DeepSeek TUI

# Check 3: view stats for an agent
token-stats -a claude-code --month
# Example output:
# 📊 Claude Code
#   deepseek-v4-flash | 入 6.44M  | 出 320.28K | 缓 27.86M (81.2%)   | 总计/+缓存 6.76M/34.62M    | 调用 1313 次
#   deepseek-v4-pro   | 入 13.12M | 出 6.36M   | 缓 2471.2M (99.5%)  | 总计/+缓存 19.47M/2490.67M | 调用 11835 次
#   合计              | 入 19.66M | 出 6.68M   | 缓 2499.06M (99.2%) | 总计/+缓存 26.34M/2525.4M  | 调用 13153 次
```

If all three checks produce output, installation is successful 🎉

## Updating

```bash
clawhub update agent-usage-stats
token-stats --version
```

> `update` replaces files in-place — wrapper and PATH carry over, no re-setup required.

> 💡 Version not changing? Use `--force` to pull the latest:
> ```
> clawhub install agent-usage-stats --force
> ```


## Usage

### Quick Reference

| What you want to do | Command | Scope |
|---------------------|---------|-------|
| Check today's token usage | `token-stats --all -t` | **All agents** |
| Check this month's usage | `token-stats --all -m` | **All agents** |
| View Claude Code only | `token-stats -a claude-code` | **Single agent** |
| Current snapshot / detail | `token-stats -a claude-code --now` / `--detail` | **Single agent** |
| Real-time monitoring | `token-stats -a claude-code -w` | **Single agent** |
| Compare last week vs this week | `token-stats -a claude-code --compare --a last-week --b this-week` | **Single agent** |
| Export to Excel | `token-stats -a claude-code -m -e` | **Single / All agents** |
| List detected agents | `token-stats --list-backends` | Current device |
| Update / uninstall | `token-stats update` / `token-stats --uninstall` | Tool maintenance |
| Interactive menu | `token-stats` | Interactive |

### Common Options

| Short | Long | What it does |
|:---:|---|---|
| `-a` | `--agent` | Pick which agent: `claude-code` / `codex` / `hermes` / `openclaw` / `reasonix` / `deepseek-tui`. Use commas for multiple |
| `-t` | `--today` | Today only |
| | `--yesterday` | Yesterday only |
| | `--week` | This week, starting Monday |
| | `--last-7d` | Last 7 days |
| `-m` | `--month` | This month (1st to today) |
| `-y` | `--year` | This year (Jan 1 to today) |
| | `--from` / `--to` | Custom date range, `YYYY-MM-DD` |
| `-w` | `--watch` | Live monitor, refreshes every 5 seconds, Ctrl+C to stop |
| `-e` | `--export` | Export to XLSX / CSV / JSON file |
| `-v` | `--version` | Show version number |
| `-l` | `--list-backends` | List installed AI assistants |
| | `--compare` / `--a` / `--b` | Compare two periods |
| | `--now` / `--detail` | Current snapshot / detail mode, same as default stats |
| `--all` | | View **all** agents at once |
| | `setup` / `--setup` | Install to `~/.token-stats/`, create `~/.token-stats/bin/token-stats`, and add it to PATH |
| | `update` / `--update` | Update to the latest version |
| | `--uninstall` | Remove wrapper, install directory, and PATH entry |

> Short options can be combined. For example, `-a claude-code -t -e` means "Claude Code only, today, export."
> Example outputs below are anonymized examples. Your numbers will differ by agent, model, timezone, and usage.

---

### 1. View a Single Agent

Replace `claude-code` with your agent (`codex` / `hermes` / `openclaw` / `reasonix` / `deepseek-tui`).

**All history (no time filter):**
```bash
token-stats -a claude-code
```

**Current snapshot / detail mode (same as default stats):**
```bash
token-stats -a claude-code --now
token-stats -a claude-code --detail
```

**Today only:**
```bash
token-stats -a claude-code -t
```

**Yesterday:**
```bash
token-stats -a claude-code --yesterday
```

**This month (1st to today):**
```bash
token-stats -a claude-code -m
```

**This year (Jan 1 to today):**
```bash
token-stats -a claude-code --year
```

**This week (Monday to today):**
```bash
token-stats -a claude-code --week
```

**Last 7 days:**
```bash
token-stats -a claude-code --last-7d
```

**Custom date range:**
```bash
# From May 1 to May 28
token-stats -a claude-code --from 2026-05-01 --to 2026-05-28
```

Example output (`token-stats -a claude-code --month`):
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

### 2. View Multiple Agents

**Pick specific agents (comma-separated):**
```bash
# Hermes and Claude Code, this month
token-stats -a hermes,claude-code -m
```

**All agents on this machine:**
```bash
# All history
token-stats --all

# All agents, today
token-stats --all -t

# All agents, this month
token-stats --all -m

# All agents, this year
token-stats --all --year
```

Example output (`token-stats --all --month`):
```
📊 本机 Agent 统计汇总
══════════════════════════════════════════════════

✅ Claude Code
📊 Claude Code
  deepseek-v4-flash | 入 439.99K | 出 21.11K  | 缓 1.81M (80.5%)  | 总计/+缓存 461.1K/2.27M   | 调用 60 次  | ≈¥0.52
  deepseek-v4-pro   | 入 733.74K | 出 122.12K | 缓 24.45M (97.1%) | 总计/+缓存 855.86K/25.31M | 调用 176 次 | ≈¥3.55
  合计              | 入 1.17M   | 出 143.23K | 缓 26.26M (95.7%) | 总计/+缓存 1.32M/27.58M   | 调用 236 次 | ≈¥4.06 (仅供参考)

✅ CodeX
📊 CodeX
  gpt-5.5           | 入 7.54M   | 出 633.52K | 缓 99.93M (93.0%) | 总计/+缓存 8.17M/108.11M | 调用 1082 次 | ≈¥2222.39
  codex-auto-review | 入 129.86K | 出 3.2K    | 缓 915.58K (87.6%) | 总计/+缓存 133.06K/1.05M | 调用 23 次   | ≈¥0.00
  deepseek-v4-flash | 入 16.32K  | 出 816     | 缓 63.87K (79.6%)  | 总计/+缓存 17.14K/81.01K | 调用 6 次    | ≈¥0.02
  合计              | 入 7.69M   | 出 637.54K | 缓 100.91M (92.9%) | 总计/+缓存 8.32M/109.23M | 调用 1111 次 | ≈¥2222.41 (仅供参考)

✅ Hermes
Hermes: 该时间段内无会话记录

✅ Reasonix
Reasonix: usage.jsonl 中无有效数据

✅ DeepSeek TUI
DeepSeek TUI: 尚无会话记录

══════════════════════════════════════════════════
  全部 Agent 总计
  入 8.86M | 出 780.77K | 缓 127.17M (93.5%) | 总计/+缓存 9.64M/136.82M | 调用 1347 次 | ≈¥2226.47 (仅供参考)
```

---

### 3. List Installed AI Assistants
```bash
token-stats -l
# or
token-stats --list-backends
```

Output shows which agents are detected (✅) and which are not (❌).

---

### 4. Compare Two Time Periods

Side-by-side comparison showing input/output/cache/total/total_with_cache/calls for each model, with a delta column.

**Yesterday vs today:**
```bash
token-stats -a claude-code --compare --a yesterday --b today
```

**Last week vs this week:**
```bash
token-stats -a claude-code --compare --a last-week --b this-week
```

**Last month vs this month:**
```bash
token-stats -a claude-code --compare --a last-month --b this-month
```

**Last year vs this year:**
```bash
token-stats -a claude-code --compare --a last-year --b this-year
```

**Two custom dates:**
```bash
# Two specific days
token-stats -a claude-code --compare --a 2026-01-01 --b 2026-01-15

# Two date ranges (connected with ~)
token-stats -a claude-code --compare --a 2026-01-01~2026-01-07 --b 2026-01-08~2026-01-14
```

Supported labels: `today` / `yesterday` / `this-week` / `last-week` / `this-month` / `last-month` / `this-year` / `last-year` / `YYYY-MM-DD` / `YYYY-MM-DD~YYYY-MM-DD`

Example output (`token-stats -a codex --compare --a last-week --b this-week`):
```
📊 对比: 2026-05-25~2026-05-31 vs 2026-06-01~2026-06-07  [CodeX]
===============================================================================================
  模型       | 指标         | 2026-05-25~2026-05-31 | 2026-06-01~2026-06-07 | 变化
───────────────────────────────────────────────────────────────────────────────────────────────
  gpt-5.5    | 总计         | 5.3M                  | 8.18M                 | +2.88M
             | 总计(含缓存) | 69.63M                | 108.18M               | +38.55M
             | 调用         | 878                   | 1083                  | +205
             | 费用         | ≈¥1438.90             | ≈¥2223.81             | +¥784.91
  合计       | 入           | 4.93M                 | 7.69M                 | +2.76M
             | 出           | 447.74K               | 637.77K               | +190.03K
             | 缓           | 64.56M                | 100.98M               | +36.42M
             | 总计         | 5.38M                 | 8.33M                 | +2.95M
             | 调用         | 888                   | 1112                  | +224
             | 费用         | ≈¥1438.90             | ≈¥2223.83             | +¥784.93
───────────────────────────────────────────────────────────────────────────────────────────────
```

---

### 5. Real-time Monitoring

Watch token usage in real time as you chat with the agent. Press Ctrl+C to stop and see a summary.

**Default 5-second refresh:**
```bash
token-stats -a claude-code -w
```

**Custom interval (e.g., 2 seconds):**
```bash
token-stats -a claude-code -w 2
```

> Watch mode only supports a **single** agent.

---

### 6. Export to File

Three formats: XLSX (Excel), CSV, JSON. Yearly exports automatically split by month.

**Export a single agent:**
```bash
# All history (prompts for format and directory)
token-stats -a claude-code -e

# Today
token-stats -a claude-code -t -e

# This month
token-stats -a claude-code -m -e

# This year (auto-split by month)
token-stats -a claude-code --year -e

# Specify output directory directly
token-stats -a claude-code -m -e ~/Desktop
```

**Export all agents:**
```bash
# All agents, this month
token-stats --all -m -e

# All agents, this year (monthly columns, single sheet)
token-stats --all --year -e
```

**Choosing format non-interactively:**
```bash
# XLSX (press Enter = default)
echo 1 | token-stats -a claude-code -m -e ~/Desktop

# CSV
echo 2 | token-stats -a claude-code -m -e ~/Desktop

# JSON
echo 3 | token-stats -a claude-code -m -e ~/Desktop
```

---

### 7. Interactive Menu

Run without arguments to pick an agent from a menu:
```bash
token-stats
```

---

### 8. Tool Maintenance

**Show help (all commands):**

```bash
token-stats --help
```

**Show current version:**

```bash
token-stats -v
# or
token-stats --version
```

**Update to the latest version:**

```bash
token-stats update
```

If the version doesn't change after update, force reinstall:

```bash
clawhub install agent-usage-stats --force
```

**Uninstall token-stats:**

```bash
token-stats --uninstall
```

**Run setup after ClawHub install:**

```bash
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

---

### What each agent shows

| Agent | Snapshot | Time range |
|-------|----------|------------|
| **Hermes** | Input/output/cache + calls + session count | Total + session count |
| **Claude Code** | Total + input/output/cache + calls + sub-agents/projects | Same |
| **CodeX** | Input/output/cache + calls + cache rate + estimated cost | Same |
| **OpenClaw** | Input/output/cache + calls | Total + calls |
| **Reasonix** | Input/output/cache + calls + cache rate + estimated cost | Same |
| **DeepSeek TUI** | Total + sessions + tool calls + estimated cost | Same |

### Data sources

| Agent | Reads from |
|-------|-----------|
| Hermes | `~/.hermes/state.db` → sessions table |
| Claude Code | `~/.claude/projects/**/*.jsonl` |
| CodeX | `~/.codex/state_*.sqlite` → threads table + `~/.codex/sessions/**/*.jsonl` → token_count events |
| OpenClaw | `~/.openclaw/agents/main/sessions/` |
| Reasonix | `~/.reasonix/usage.jsonl` |
| DeepSeek TUI | `~/.deepseek/sessions/*.json` |

### Windows + WSL2

When your agent runs inside WSL2, `token-stats` automatically detects and reads data from the Windows side. Even if Hermes is running (database locked), it reads via `wsl.exe` internally; output is labeled `(WSL)`.

1. **WSL distro must be running** — open a WSL terminal first
2. **Username agnostic** — auto-detects the WSL user's home directory
3. **Proxy unaffected** — VPN/proxy only affects WSL networking, not local file access

### Model name handling

`token-stats` groups usage by the model name already recorded by each Agent. Known names can use configured pricing metadata; unknown names still appear in the summary and are excluded from estimated cost until pricing is configured.

---

## Common Scenarios

**How much did I spend today?**
```bash
token-stats --all --today
```

**This month — all agents summary**
```bash
token-stats --all --month
```

**This month — all agents export**
```bash
token-stats --all --month --export
```

**This year — all agents export**
```bash
token-stats --all --year --export
```

**This week vs last week**
```bash
token-stats -a hermes --compare --a last-week --b this-week
```

**This month vs last month**
```bash
token-stats -a hermes --compare --a last-month --b this-month
```

**Watch consumption in real time**
```bash
token-stats -a hermes --watch
# Switch to Hermes, watch tokens update live
```

**Multiple agents + time range**
```bash
token-stats -a hermes,claude-code --month
```

---

## Uninstall

```bash
# Step 1: Clean up global command + PATH (automatic)
token-stats --uninstall
```

> `--uninstall` automatically removes wrappers, cleans PATH entries, deletes config files, removes `~/.token-stats/`, and clears ClawHub/history install directories such as `~/skills/agent-usage-stats` so reinstall can start cleanly. Works on all platforms.

---

## Compatibility

| Platform | Status |
|----------|--------|
| macOS | ✅ Full support |
| Linux | ✅ Full support |
| Windows | ✅ Supported (`.cmd` wrapper) |

| Requirement | Details |
|-------------|---------|
| Python | 3.11+ (stdlib only, no pip dependencies) |
| Node.js | Required only for installation (ClawHub CLI) |

---

## Troubleshooting

### Installation issues

#### ❓ `clawhub install agent-usage-stats` fails

**Possible cause: network issue or outdated Node.js.**

```bash
# Check Node.js version (needs v18+)
node --version

# Reinstall ClawHub
npm install -g clawhub

# In China with slow network:
npm install -g clawhub --registry=https://registry.npmmirror.com
```

<a id="setup-not-found"></a>
#### ❓ Install path troubleshooting

**When: `setup` fails with file not found.**

**Cause: `clawhub install` was run from a different directory (not home).** Skills are placed under `./skills/` relative to the working directory.

**Fix:**
```bash
cd ~
clawhub install agent-usage-stats --force
```

Then follow the install steps above. The home directory (`~`) is always writable on all OSes.

<a id="ps-tilde"></a>
#### ❓ PowerShell: `can't open file '...~...'`

**Cause: PowerShell does not expand `~` when passed as a command argument**, treating it as a literal directory name.

Error example:
```
python: can't open file 'C:\\Users\\xxx\\~\\skills\\...': No such file or directory
```

**Fix: use `$HOME` instead of `~`:**
```powershell
# ❌ Wrong
python ~\skills\agent-usage-stats\token-stats.py setup

# ✅ Correct
python $HOME\skills\agent-usage-stats\token-stats.py setup
```

> `$HOME` is a built-in PowerShell variable that always expands to the current user directory.

#### ❓ `token-stats` command not found

**Cause 1: Haven't run `setup` yet** → Follow the ClawHub install steps above.

**Cause 2: Ran `setup` but haven't opened a new terminal** → `setup` writes PATH to system config. Open a new terminal for it to take effect.

**Cause 3: `setup` PATH write failed** → Re-run `setup` and check for errors. If needed, add PATH manually:

**macOS (zsh):**
```bash
echo 'export PATH="$HOME/.token-stats/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Linux (bash):**
```bash
echo 'export PATH="$HOME/.token-stats/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell, current session only):**
```powershell
$env:PATH += ';' + "$env:USERPROFILE\.token-stats\bin"
```

#### ❓ `Permission denied` when running `token-stats`

**macOS / Linux only. Cause: wrapper script lacks execute permission.**

```bash
chmod +x ~/.token-stats/bin/token-stats
# Or just re-run setup
python3 ~/skills/agent-usage-stats/token-stats.py setup
```

> Windows users are not affected (`.cmd` files don't need execute permission).

### Runtime issues

#### ❓ My agent isn't showing in the menu

**Cause: `token-stats` checks for specific config files.** These paths must exist:

| Agent | Detection path |
|-------|---------------|
| **Hermes** | `~/.hermes/state.db` |
| **Claude Code** | `~/.claude/projects/` |
| **CodeX** | `~/.codex/state_*.sqlite` |
| **OpenClaw** | `~/.openclaw/agents/main/sessions/sessions.json` |

Run `token-stats --list-backends` to see what's detected.

#### ❓ Stats show "no data" or all zeros

**Possible causes:**

1. **Agent is installed but never used** → use it first, then check again
2. **Data file path is wrong** → confirm with `token-stats --list-backends`
3. **Time range has no data** → if using `--today` or `--from`, check that sessions exist in that period

#### ❓ `unknown` model appears in compare results

**Hermes DB has sessions with empty model field** — doesn't affect accuracy. Diagnose with:

```bash
sqlite3 ~/.hermes/state.db "SELECT DISTINCT model FROM sessions WHERE model IS NULL OR model = ''"
```

> Windows users without `sqlite3` can use Python instead:
> ```powershell
> python3 -c "import sqlite3; c=sqlite3.connect(r'$env:USERPROFILE\.hermes\state.db'); print('\n'.join(r[0] or '(NULL)' for r in c.execute('SELECT DISTINCT model FROM sessions WHERE model IS NULL OR model = \"\"')))"
> ```

#### ❓ Export says "directory not found"

**Cause: the directory path you entered doesn't exist.** Create it first:

```bash
mkdir -p ~/Desktop/my-data
token-stats -a hermes --export
# Enter: ~/Desktop/my-data
```

#### ❓ Install successful but `token-stats` command not found

**Cause:** `clawhub install` was run from a directory other than home, or your system has `~/.openclaw/` (which redirects ClawHub's install target).

**Fix for all OSes:**
```bash
cd ~
clawhub install agent-usage-stats --force
python3 ~/skills/agent-usage-stats/token-stats.py setup
token-stats --version
```

This ensures the tool is installed to `~/.token-stats/` — the predictable home-directory location.

#### ❓ OpenClaw shows calls but zero tokens

**Cause:** Some OpenClaw versions (especially older builds on Linux) don't record token usage (`input`/`output` counts) in their data files. The tool detects session files and model names, but the `usage` field in `.jsonl` is populated as `0`.

**Notable data:** 0 tokens + non-zero call count → confirms usage recording is missing at the source.

**Resolution:** This is an OpenClaw data recording limitation, not a token-stats bug. Token-stats reads whatever the agent wrote down. Options:
- Upgrade OpenClaw to a newer version that records token usage
- No workaround available in token-stats itself

#### ❓ `--compare` shows no data for both periods

**Possible cause:** neither period has session records. Check with `--today` first.

### Data scope

> ⚠️ `token-stats` **only reads local data. No cross-machine aggregation.**
>
> - **Same API key on multiple machines? → Each machine's stats are isolated**
> - Example: Same key used on PC A and PC B → PC A's `token-stats` only sees PC A's usage
> - `token-stats` reads disk files — no network calls, no API dashboard queries
> - To see another machine's stats, install `token-stats` there too
>
> 🕐 **Timezone**: `--today` / `--yesterday` use your **local system timezone**. E.g. on UTC+8 (Beijing), `--today` spans 00:00–23:59 CST. Machines in different timezones see different ranges.

### API Relay

Stats accuracy depends on whether the relay **passes through** the real API's `usage` field unchanged. `token-stats` reads what your Agent wrote locally — it does not verify against the real API.

### How It Works

`token-stats` reads local data files (SQLite / JSONL) written by each Agent, aggregating `input_tokens`, `output_tokens`, `cache_read_tokens`, and call counts from the `usage` object.

```
API returns usage → Agent writes locally → token-stats reads & aggregates
```

Results may differ from your API billing dashboard because:
- **Cache tokens** may be counted multiple times (once per cache hit)
- **Agent recording gaps** — some Agents/versions don't record all fields
- **Timezone mismatch** — API dashboards use UTC, this tool uses local time
- **Relay modification** — some relays alter or drop the `usage` field

> This is a **local ledger** — it shows what your Agent recorded, not the upstream billing.
