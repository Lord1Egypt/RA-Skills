# Work Log Format Specification

## File Naming

```
~/.workbuddy/work-logs/YYYY-MM-DD.md
```

One file per calendar day, even if no work was recorded (empty days are handled
at report-generation time).

## File Structure

```markdown
# YYYY-MM-DD DayOfWeek

## 工作记录
- [HH:MM] 【Category】Description
- [HH:MM] 【Category】Description
```

### Header

The first line is a level-1 heading: `# YYYY-MM-DD DayOfWeek`

Where `DayOfWeek` is one of: 周一, 周二, 周三, 周四, 周五, 周六, 周日.

### Section

The second-level heading `## 工作记录` marks the entries section. All entries go
under this heading.

### Entry Format

```
- [HH:MM] 【Category】Description
```

| Component | Format | Example |
|-----------|--------|---------|
| Time | `HH:MM` 24-hour | `14:30` |
| Category | `【Tag】` | `【开发】` |
| Description | Chinese, one sentence | `完成用户模块API重构` |
| Separator | Space between `]` and `【` | `] 【` |

### Category Tags (Closed Set)

| Tag | Scope |
|-----|-------|
| `【开发】` | Writing/refactoring code |
| `【会议】` | Meetings and discussions |
| `【文档】` | Documentation and specs |
| `【修bug】` | Bug fixes |
| `【评审】` | Code and design review |
| `【学习】` | Research and self-study |
| `【运维】` | Deploy, CI/CD, infra |
| `【沟通】` | Async communication |
| `【规划】` | Planning and estimation |
| `【其他】` | Miscellaneous |

## Constraints

- Maximum one file per date.
- All entries in chronological order within the file.
- Description is a single line. No multi-line entries.
- No nested lists or sub-bullets within entries.
- Descriptions are plain text, no Markdown formatting except for inline code if needed.
- The `【Category】` tag is mandatory. No untagged entries.
