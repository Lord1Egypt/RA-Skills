# doc-formatter Skill — Quick Start Guide

## Install the Skill

Place the `doc-formatter` folder in your `Desktop/skills/` directory, then type in Claude Code:

```
/doc-formatter
```

The skill loads automatically.

## Quick Command Reference

### 1️⃣ View All Templates

```bash
/doc-formatter list-templates
```

### 2️⃣ Preview a Template Structure

```bash
# Preview the Notice template
/doc-formatter preview notice

# Preview the Request template
/doc-formatter preview request
```

### 3️⃣ Generate a Document

**Method 1: Interactive (Recommended)**

```bash
/doc-formatter new notice
```
The system will guide you step by step through title, recipient, purpose, details, signature, etc., and generate a complete document.

**Method 2: One-Step (when all info is ready)**

```bash
# Notice
/doc-formatter new notice --title="关于2026年端午节放假安排的通知" --recipient="全体员工"

# Request for Approval
/doc-formatter new request --title="关于审批信息化建设项目的请示" --recipient="公司领导"

# Meeting Minutes
/doc-formatter new minutes --title="关于AI大模型平台建设推进会的会议纪要"

# Work Summary
/doc-formatter new summary --title="2026年上半年工作总结"
```

### 4️⃣ Adjust Output Style

```bash
# Concise style (bullet-point, suitable for internal)
/doc-formatter new notice --style=concise

# Detailed style (full version, suitable for external submission)
/doc-formatter new report --style=detail
```

### 5️⃣ Export

```bash
# Export as Markdown file to desktop
/doc-formatter export ./2026年上半年工作总结.md
```

## Usage Scenarios

### Scenario 1: Write a Meeting Notice

```bash
/doc-formatter new meeting-notice

# Fill in sequentially:
# Title: Notice on Convening 2026 Q2 Work Summary Meeting
# Time: June 20, 14:00
# Venue: 3F Conference Room
# Attendees: All department heads
# Agenda: Department reports, leadership summary speech
# Requirements: Prepare report materials in advance
```

### Scenario 2: Write a Request for Approval

```bash
/doc-formatter new request

# Fill in sequentially:
# Title: Request for Approval of AI Computing Server Procurement
# Recipient: Company Leadership
# Background: Current computing power insufficient, affecting model training
# Request: Procure 2 AI computing servers
# Budget: ¥3,000,000
```

### Scenario 3: Write a Work Summary

```bash
/doc-formatter new summary

# Fill in main work, achievements, issues, plans
# Automatically generates a well-structured summary
```

### Scenario 4: Write Meeting Minutes

```bash
/doc-formatter new minutes

# Fill in time, venue, attendees, agenda items
# Automatically formatted as standard meeting minutes
```

## Best Practices

1. **First use**: Run `list-templates` to see all available templates
2. **Preparation**: Sort out key information points before starting interactive mode
3. **Style**: Use `--style=concise` for internal, `--style=detail` for external submissions
4. **Refinement**: After generation, ask for wording adjustments or paragraph additions/deletions
5. **Export**: Export Markdown, then copy to Word/WPS for final formatting
6. **Customization**: Edit `references/phrase-library.md` for personalized phrasing

## Adding New Templates

To add a new document template:

1. Add the template structure to `references/template-library.md`
2. Add corresponding phrases to `references/phrase-library.md`
3. The `list-templates` command will auto-detect the new template

## Tips

- 💡 After generation, just tell the system what to change — it will update the document
- 💡 Fixed phrases can be customized to match your organization's conventions
- 💡 Classified/confidential documents should NOT be processed through this tool
- 💡 Always manually review generated documents before official stamping