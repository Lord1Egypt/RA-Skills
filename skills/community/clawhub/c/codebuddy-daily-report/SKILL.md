---
name: daily-report
description: >
  Generate a daily work report by automatically discovering all git repositories
  the user worked on, collecting commit logs across all branches,
  and summarizing CodeBuddy Agent session overviews. Supports any date via
  --date, --yesterday, or --days-ago flags. Use this skill when the user
  asks to generate a daily report, work summary, daily log, 日报, 工作日报,
  今日工作总结, 昨日工作总结, or any variation of "what did I do today/yesterday".
---

# Daily Work Report Generator

## Overview

This skill automatically discovers all git repositories the user committed to,
collects commit history across ALL branches, gathers CodeBuddy Agent session overviews,
and generates a structured daily work report. It works cross-platform (macOS, Linux, Windows)
with zero configuration required. Supports generating reports for **any date** (today,
yesterday, or a specific date).

## Step-by-Step Workflow

### Step 1: Run the data collection script

Execute the bundled Python script to collect all raw data:

```bash
# Today (default)
python "SKILL_DIR/scripts/collect.py"

# Yesterday
python "SKILL_DIR/scripts/collect.py" --yesterday

# Specific date
python "SKILL_DIR/scripts/collect.py" --date 2026-03-20

# N days ago
python "SKILL_DIR/scripts/collect.py" --days-ago 3
```

Replace `SKILL_DIR` with the actual path to this skill's directory
(e.g., `~/.codebuddy/skills/daily-report`).

**Date selection rules:**
- If the user says "今天" / "today" → no extra flags (default)
- If the user says "昨天" / "yesterday" → use `--yesterday`
- If the user says a specific date → use `--date YYYY-MM-DD`
- If the user says "前天" / "the day before yesterday" → use `--days-ago 2`
- If the user says "N天前" → use `--days-ago N`

The script will:
- Auto-detect the operating system
- Find common development directories
- Discover all git repos with commits on the target date (across ALL branches)
- Collect CodeBuddy Agent session overviews modified on the target date
- Output structured JSON to stdout

If the user has a custom config file at `SKILL_DIR/references/config.yaml`,
the script will also read extra search directories and preferences from it.

### Step 2: Parse the JSON output

The script outputs JSON with this structure:

```json
{
  "date": "2026-03-25",
  "system": "Darwin",
  "git_author": "username",
  "repos": [
    {
      "path": "/path/to/repo",
      "name": "repo-name",
      "commits": [
        {
          "hash": "abc1234",
          "message": "feat: add login page",
          "branch": "feature/login",
          "time": "2026-03-25 14:30:00"
        }
      ],
      "diff_stats": "+150 -30 across 8 files"
    }
  ],
  "agent_sessions": [
    {
      "session_id": "abc123",
      "overview_content": "...",
      "modified_time": "2026-03-25 16:00:00"
    }
  ],
  "errors": []
}
```

### Step 3: Generate the daily report

Using the collected data, generate a well-structured daily report in the user's language
(default: Chinese if the user speaks Chinese, otherwise English).

Follow this structure:

#### Report Template

```markdown
# 工作日报 - {date}

## 📊 今日概览
- 活跃仓库: {count} 个
- 总提交数: {count} 次
- 代码变更: +{additions} -{deletions}

## 🔧 项目详情

### {repo-name-1}
**分支**: {branch-names}

| 时间 | 提交说明 |
|------|---------|
| HH:MM | commit message |

**代码统计**: +{add} -{del}, {files} 个文件

### {repo-name-2}
...

## 🤖 AI 辅助工作
{Summary of Agent session overviews, grouped by project}

## 📝 今日总结
{A 2-3 sentence high-level summary of the day's work}
```

### Step 4: Save the report

Save the generated report to the user's workspace or a location they specify.
Default filename: `daily-report-{YYYY-MM-DD}.md`

## Important Notes

- The script requires only Python 3.6+ standard library and git CLI — no pip install needed.
- If the script finds no commits, inform the user and suggest checking if git author name is correct.
- If the user wants to customize search directories, guide them to edit `references/config.yaml`.
- Always present the report in the user's preferred language.
- When summarizing Agent sessions, focus on what was accomplished, not implementation details.
- Group related commits across repos into coherent work items when possible.
