---
name: fcalendar-skill
description: fcalendar-skill is a Chinese date/time expression recognition and holiday query tool. **Trigger this skill whenever users mention any time-related terms**, including but not limited to: 明天, 后天, 下周, 春节, 国庆节, Christmas, Monday, etc. It can identify and annotate time expressions in natural language text (Chinese and English), resolve them to exact calendar dates, and query Chinese public holidays and normal weekends within a specified time range. Use this skill when users ask about dates, time expressions, schedules, holidays, or when you need to resolve relative time references to concrete dates.
license: See LICENSE.txt
allowed-tools: "Read Exec"
compatibility: "Requires Python 3.7+. Supports Linux, macOS, and Windows systems."
---

# fcalendar

Use `fcalendar` to identify time expressions in text and query Chinese public holiday schedules.  
All commands output **single-line JSON** to `stdout`; errors go to `stderr`.

> [!IMPORTANT]
> **Always invoke fcalendar as `python3 -m fcalendar ...`** — this bypasses all PATH issues and works
> regardless of virtual environments, system Python, or installation prefix. Never rely on the bare
> `fcalendar` command being on PATH.

## Quick Start

1. **Check if already installed** (do this first — skip install if it succeeds):
   ```bash
   python3 -c "import fcalendar; print('fcalendar installed, version:', fcalendar.__version__)"
   ```
   If this prints a version number, skip to step 3.

2. **Install** (only if step 1 failed):
   
   > [!NOTE]
   > **Package Source**: The `fcalendar` package is available on PyPI at https://pypi.org/project/fcalendar/
   > 
   > **Source Code**: You can review the source code at https://github.com/youngfreefjs/fcalendar
   > 
   > **Security**: This package only performs local date/time parsing and does not access network resources or collect user data.
   
   ```bash
   python3 -m pip install fcalendar 
   ```
   
   For enhanced security, consider installing in a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   python3 -m pip install fcalendar
   ```

3. **Verify**:
   ```bash
   python3 -m fcalendar --help
   ```
   Confirm help output is shown. If this fails but step 1 succeeded, the package is installed but
   may not support `-m` invocation — fall back to the full binary path:
   ```bash
   $(python3 -c "import sys, os; print(os.path.join(sys.prefix, 'bin', 'fcalendar'))") --help
   ```

4. **Get current date** when needed: `date +%Y-%m-%d`

> [!NOTE]
> **Invocation rule**: In all commands below, replace `fcalendar` with `python3 -m fcalendar`.
> Example: `fcalendar query "明天"` → `python3 -m fcalendar query "明天"`

## Core Capabilities

### 1. Time Expression Recognition — `query`

Identifies and annotates time expressions in natural language, resolving them to exact dates.

**Command:**
```
fcalendar query "<text>" [--today YYYY-MM-DD] [--lang zh|en]
```

**Arguments:**
| Argument | Required | Description |
|----------|----------|-------------|
| `<text>` | yes | Natural language text containing time expressions |
| `--today` | no | Reference date (YYYY-MM-DD). Defaults to system date |
| `--lang` | no | Language: `zh` or `en`. Defaults to auto-detect |

**Output:**
```json
{"input": "下周开会", "result": "下周开会（今天是2026年3月31日，下周是2026年4月6日至12日）"}
```

**Examples:**
```bash
fcalendar query "明天下午三点开会"
fcalendar query "国庆节去旅游" --today 2026-09-01
fcalendar query "meeting next Monday" --lang en
fcalendar query "春节回家" --today 2026-01-15
```

**Supported time expression types:**

For a comprehensive list of all supported time expression types with detailed examples, see [references/time-expressions.md](references/time-expressions.md).

Key categories include:
- Relative days (明天、后天、tomorrow)
- Relative weeks (本周一、下周五、next Monday)
- Chinese holidays (春节、国庆节、清明节)
- Lunar festivals (元宵节、七夕、除夕)
- Western festivals (Christmas、Halloween、Valentine's Day)
- 24 solar terms (春分、冬至、立春)
- And many more...

---

### 2. Holiday Query — `holiday`

Queries public holidays and normal weekends within a specified time range. Excludes workdays-on-weekends (调休上班) to avoid confusion.

> For detailed information about Chinese public holidays and solar terms, see [references/holidays.md](references/holidays.md).

**Command:**
```
fcalendar holiday [--scope <scope>] [--today YYYY-MM-DD]
```

**Arguments:**
| Argument | Required | Default | Description |
|----------|----------|---------|-------------|
| `--scope` | no | `half_year` | Time range (see below) |
| `--today` | no | system date | Reference date (YYYY-MM-DD) |

**Supported scope values (Chinese and English both accepted):**

| Scope | Alias | Description |
|-------|-------|-------------|
| `half_year` | `半年`, `未来半年` | Next 180 days (default) |
| `this_week` | `本周`, `这周` | Mon–Sun of current week |
| `next_week` | `下周`, `下一周` | Mon–Sun of next week |
| `next_month` | `下个月`, `下一个月`, `下月` | Full next calendar month |
| `weeks=N` | `N周`, `未来N周` | Next N weeks from today |
| `months=N` | `N个月`, `未来N个月` | Next N months from today |

N supports Chinese numerals: 一、两、三、四...十二, and Arabic numerals.

**Output:** JSON array, sorted by `start` date ascending.

```json
[
  {"type": "holiday", "name": "劳动节", "start": "2026-05-01", "end": "2026-05-05", "days": 5},
  {"type": "weekend", "name": "周末",   "start": "2026-05-09", "end": "2026-05-10", "days": 2}
]
```

**Output fields:**
| Field | Type | Description |
|-------|------|-------------|
| `type` | string | `"holiday"` = Chinese public holiday; `"weekend"` = normal restful weekend |
| `name` | string | Holiday name (e.g. `"春节"`, `"周末"`) |
| `start` | string | Start date, ISO format (YYYY-MM-DD) |
| `end` | string | End date, ISO format (YYYY-MM-DD) |
| `days` | int | Number of days |

> Note: Workdays-on-weekends (调休上班) are NOT included in the output. The list only shows days off.

**Examples:**
```bash
fcalendar holiday                          # next 180 days (default)
fcalendar holiday --scope this_week        # this week
fcalendar holiday --scope 本周             # same as above (Chinese)
fcalendar holiday --scope next_week        # next week
fcalendar holiday --scope next_month       # next full month
fcalendar holiday --scope weeks=3          # next 3 weeks
fcalendar holiday --scope 三周             # same as weeks=3 (Chinese numeral)
fcalendar holiday --scope months=2         # next 2 months
fcalendar holiday --scope 未来两个月       # same as months=2
fcalendar holiday --scope half_year --today 2026-09-01  # 180 days from Sep 1
```

---

## Friendly Display Requirements

> [!IMPORTANT]
> **Strict Output Rule**: Always use the exact content returned by the `fcalendar` CLI.
> Do NOT paraphrase, rewrite, supplement, or infer beyond what the CLI returns.
> The `result` field (for `query`) and the JSON array (for `holiday`) are the single
> source of truth. Present them as-is after formatting; never modify their semantic content.

- **General principle**: output must be valid Markdown with clear structure.
- **For `query`**: display the `result` field directly as the annotated response. Do not display raw JSON to the user.
- **For `holiday`**:
  - Group results by `type`: list `holiday` entries first, then `weekend` entries.
  - Use a Markdown table or bullet list to present each item.
  - Highlight key facts: name, date range, number of days.
  - If the result is empty, tell the user there are no holidays in that period.

### Recommended output structure for `holiday`

```
## 放假安排（[scope描述]）

### 法定节假日
| 假期 | 开始 | 结束 | 天数 |
|------|------|------|------|
| 劳动节 | 2026-05-01 | 2026-05-05 | 5天 |

### 普通周末
| 日期 | 天数 |
|------|------|
| 2026-04-25 ~ 2026-04-26 | 2天 |
```

### Error handling

- If the `--scope` value is invalid, the CLI exits with a non-zero code and prints an error to `stderr`. Inform the user of valid scope formats.
- Always get the current date with `date +%Y-%m-%d` before calling if real-time accuracy is required.
