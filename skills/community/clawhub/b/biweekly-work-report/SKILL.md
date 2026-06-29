---
name: biweekly-work-report
description: "Record daily work items into structured logs and generate weekly biweekly reports from accumulated data. Trigger when the user says 记录工作 记录一下 今天做了 生成周报 本周周报 双周报 工作汇报 周报 or any variation of logging work or producing a work report."
agent_created: true
---

# Biweekly Work Report Skill

Record daily work and generate structured weekly/biweekly reports.
All logs are plain Markdown files — readable and writable by any AI tool
(Claude Code, Cursor, Codex, WorkBuddy). No servers, no databases.

## Trigger Words

| Trigger | Action |
|---------|--------|
| 记录 / 记录一下 / 今天做了 / 记一条 | Record work item(s) |
| 生成本周周报 / 本周周报 / 周报 | Generate current week report |
| 生成上周周报 | Generate last week report |
| 生成双周报 / 双周汇报 | Generate 14-day report |
| 生成X月周报 / 生成X月~X月报告 | Generate custom date range report |

---

## Data Location

```
~/.workbuddy/work-logs/          ← canonical, never move this
├── YYYY-MM-DD.md                ← one file per day
├── YYYY-MM-DD.md
└── ...
```

Skill updates never touch data. Data is always local, always Markdown.

---

## Recording Work

### Step 1: Determine today's date

Use `YYYY-MM-DD` format in Asia/Shanghai timezone.

### Step 2: Read or create daily file

Read `~/.workbuddy/work-logs/YYYY-MM-DD.md`. If it doesn't exist, create it
with this template:

```markdown
# YYYY-MM-DD DayOfWeek

## 工作记录
```

### Step 3: Append entries

Format: `- [HH:MM] 【Category】Description`

**Categories:**

| Tag | Use For |
|-----|---------|
| `【开发】` | Coding, feature work, refactoring |
| `【会议】` | Meetings, reviews, discussions |
| `【文档】` | Docs, specs, design docs, wiki |
| `【修bug】` | Bug fixes, troubleshooting |
| `【评审】` | Code review, design review |
| `【学习】` | Research, reading, self-study |
| `【运维】` | Deployment, CI/CD, infra ops |
| `【沟通】` | Slack/IM/email discussions |
| `【规划】` | Planning, estimation, breakdown |
| `【其他】` | Miscellaneous |

**Rules:**
- Always **append**, never overwrite existing entries.
- Use the time the user provides, or current time if not stated.
- One entry per distinct activity. Split compound descriptions.
- Descriptions in Chinese, one sentence. Keep it concise.

**Examples:**

```
User: "记录：上午完成了登录模块重构"
→ Append: - [09:00] 【开发】完成登录模块重构

User: "下午开了技术评审会，然后修了一个支付回调的bug"
→ Append:
- [14:00] 【会议】参加技术方案评审会
- [16:00] 【修bug】修复支付回调签名校验失败问题
```

---

## Generating Reports

### Step 1: Determine date range

- "本周周报" → Monday through today (current week).
- "上周周报" → Monday through Friday (last week).
- "双周报" → 14 days ending today, or the most recent two calendar weeks.
- Custom range → use explicit user dates.

### Step 2: Collect data

Read all `~/.workbuddy/work-logs/YYYY-MM-DD.md` files within the date range.
Skip days with no entries or no file.

### Step 3: Generate report

Output format (see `references/report-template.md` for the full spec):

```markdown
# 工作周报 — YYYY.MM.DD ~ YYYY.MM.DD

## 一、本周重点工作
- (merge related entries into 2-5 high-level items, quantify days)

## 二、详细工作记录
### YYYY-MM-DD (DayOfWeek)
- [HH:MM] 【Category】Description
...

## 三、下周计划
- [ ] (infer from trajectory, or leave placeholder)

## 四、问题与风险
- (extract from 【修bug】entries and blocking mentions)

---
*生成时间: YYYY-MM-DD HH:MM*
```

### Step 4: Output location

Write to the **current workspace directory** (or user-specified path).
Default filename: `工作周报_YYYY-MM-DD~YYYY-MM-DD.md`.

### Report writing guidelines

- **重点工作**: Group by topic, not by category tag. Extract 2-5 themes
  that span multiple entries. Quantify (e.g. "耗时3天").
- **详细记录**: Chronological. Keep original entries verbatim.
- **下周计划**: Infer from work trajectory. If unclear, add `待补充` and
  remind the user.
- **问题与风险**: Extract from 【修bug】entries and blocking issues. If none
  found, write "暂无显著风险".

---

## Reference Files

| File | Purpose |
|------|---------|
| `references/work-log-format.md` | Detailed data format specification |
| `references/report-template.md` | Full report generation template |
| `assets/example-daily-log.md` | Sample daily work log |
| `assets/example-weekly-report.md` | Sample generated report |

---

## Cross-Tool Design

Key design decisions for multi-tool compatibility:

1. **Plain Markdown** — no databases, no proprietary formats.
2. **Fixed data path** — `~/.workbuddy/work-logs/` is canonical.
3. **Zero dependencies** — all logic in AI prompt instructions.
4. **Data-skill separation** — updating SKILL.md never touches logs.
