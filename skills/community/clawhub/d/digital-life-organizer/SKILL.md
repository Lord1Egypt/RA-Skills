---
name: Digital Life Organizer
slug: digital-life-organizer
description: Create a privacy-first digital life inventory and cleanup plan from user-supplied information only. This skill does not scan devices, cloud accounts, passwords, or files.
version: v1.1.0
tags: digital-organizing, privacy-first, productivity, digital-declutter, life-management
---

# Digital Life Organizer

Use this skill when the user wants a calm, privacy-first plan for organizing their digital life: files, subscriptions, accounts, backups, and recurring maintenance.

This is a **planning and checklist skill**. It does **not** scan a computer, read local files, connect to cloud storage, inspect passwords, sign in to accounts, or take any action outside the conversation. Work only from information the user chooses to type or paste.

## Good triggers

- "Help me organize my digital life."
- "Make a cleanup checklist for my files and cloud storage."
- "Help me inventory subscriptions without logging into anything."
- "Create a safe account-maintenance checklist."
- "Plan a backup and digital decluttering routine."

## Hard boundaries

- Do not ask for passwords, recovery codes, API keys, session cookies, private keys, or full account credentials.
- Do not claim that files, subscriptions, accounts, or passwords were scanned.
- Do not run shell commands or browser automation as part of this skill.
- Do not delete, move, cancel, or change anything for the user.
- Do not provide a security guarantee. Phrase security output as a checklist, not an audit result.

## Workflow

1. Ask the user which area they want to organize: files, subscriptions, accounts, backups, or all areas.
2. Ask for optional user-supplied inventory items. Accept rough descriptions; do not request secrets.
3. Classify each item into: keep, archive, review, cancel/close candidate, backup needed, or unclear.
4. Build a low-risk action plan with reversible first steps.
5. Add privacy notes and a "do not paste secrets" reminder.
6. Provide a maintenance cadence: weekly quick sweep, monthly subscription review, quarterly backup check, annual account review.

## Output format

Return a concise plan with these sections:

```markdown
## Digital Life Organizer Plan

### Scope
- Areas covered:
- Information source: user-supplied only

### Inventory Table
| Item | Category | Current concern | Suggested status | Next safe step |
|---|---|---|---|---|

### 30-Minute Cleanup Sprint
1.
2.
3.

### Reversible Safety Notes
- No deletion before backup.
- No password sharing.
- Confirm cancellations directly on the provider site.

### Maintenance Cadence
- Weekly:
- Monthly:
- Quarterly:
- Annual:
```

## Example response style

Be practical and conservative. If the user says "audit my passwords," reply with a checklist for improving password hygiene and suggest using a reputable password manager; do not request, store, or evaluate actual passwords.

## Usage Scenarios

1. **User input:** "I have files across Google Drive, Dropbox, iCloud, and my desktop. Help me organize without giving you access."
→ **Expected output:** Privacy-respecting organization plan — self-inventory worksheet, consolidation-decision framework, folder-structure template with naming conventions, and migration checklist you execute yourself.
2. **User input:** "I think I have 40+ subscriptions draining my bank account. Help me audit without accessing my accounts."
→ **Expected output:** Subscription audit method — bank-statement scanning guide, subscription-inventory template, cancellation-priority calculator, renegotiation scripts, and quarterly subscription-review calendar reminder setup.
3. **User input:** "My digital photos are chaos — 15 years across 4 devices and 3 cloud services. Build a cleanup plan."
→ **Expected output:** Photo-organization blueprint — consolidation strategy, de-duplication method recommendations, folder/year-tagging taxonomy, "keep or delete" decision framework, backup 3-2-1 strategy template, and 30-day cleanup sprint schedule.


### Scenario 2: 微信和手机存储告急
**User input:** "我微信占了60G手机空间，手机总提示存储不足。又不敢乱删怕删掉重要聊天记录和工作文件。怎么安全清理？"
**Expected output:** 微信存储空间清理实操——第一步：微信内设置→通用→存储空间→缓存（可直接清理，一般能清5-15G）；第二步：聊天记录管理（按文件大小排序，删掉超过100M的视频文件、过期的工作群文件、已保存到电脑的文件副本）；第三步：关闭自动下载（设置→通用→照片/视频/文件→关闭自动下载，避免群聊文件自动存手机）；第四步：把照片视频迁移到手机相册后删掉微信里的（用手机相册方便备份到iCloud/百度网盘）；第五步：定期（每月1次）清理微信存储，控制在20G以内。关键：不要清空聊天记录，逐个操作。
