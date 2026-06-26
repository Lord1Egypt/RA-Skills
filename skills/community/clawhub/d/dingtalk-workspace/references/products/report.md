# Report Reference

## Report Operations

### List Received Reports

```bash
dws report list --type received [--start-date <date>] [--end-date <date>] [--limit <N>]
```

**Parameters:**
- `--type`: `received` | `sent` | `all`
- `--start-date`: Start date (YYYY-MM-DD)
- `--end-date`: End date (YYYY-MM-DD)

**Example:**
```bash
# Today's received reports
dws report list --type received --start-date "2024-03-29" --end-date "2024-03-29"

# With details
dws report list --type received --start-date "2024-03-29" --end-date "2024-03-29" --jq '.result[] | {title: .title, sender: .senderName, createTime: .createTime}'
```

See bundled script: `scripts/report_inbox_today.py`

### List Sent Reports

```bash
dws report list --type sent [--start-date <date>] [--end-date <date>]
```

### Get Report Detail

```bash
dws report get --report-id <reportId>
```

**Example:**
```bash
dws report get --report-id "report123" --jq '.result | {title: .title, content: .content, sender: .senderName}'
```

### Create Report

```bash
dws report create --template-id <templateId> --content "<content>" [--receivers <userIds>]
```

**Example:**
```bash
# From file
dws report create --template-id "tpl123" --content @daily_report.md --receivers "user1,user2"

# Direct content
dws report create --template-id "tpl123" --content "### Today's Work\n- Task 1\n- Task 2"
```

## Template Operations

### List Templates

```bash
dws report template list
```

**Example:**
```bash
dws report template list --jq '.result[] | {name: .templateName, templateId: .templateId}'
```

### Get Template Detail

```bash
dws report template get --template-id <templateId>
```

## Statistics Operations

### Get Report Statistics

```bash
dws report stats --start-date <date> --end-date <date> [--dept-id <deptId>]
```

**Example:**
```bash
dws report stats --start-date "2024-03-01" --end-date "2024-03-31" --jq '.result | {sentCount: .sentCount, receivedCount: .receivedCount}'
```

## Common Patterns

### Daily Report Workflow

```bash
# 1. Get template
dws report template list --jq '.result[] | select(.templateName | contains("Daily")) | .templateId'

# 2. Create report
dws report create --template-id "tpl123" --content @daily_report.md --receivers "manager_userId"
```

### View All Reports from Specific Person

```bash
# Get user's sent reports
dws report list --type sent --start-date "2024-03-01" --end-date "2024-03-31" --jq '.result[] | select(.senderName == "John") | {title: .title, date: .createTime}'
```

### Check Who Hasn't Submitted Report

```bash
# Get department members
dws contact dept members --dept-id "dept123" --jq '.result[] | .name'

# Get today's senders
dws report list --type sent --start-date "2024-03-29" --end-date "2024-03-29" --jq '.result[] | .senderName'

# Compare to find missing
```
