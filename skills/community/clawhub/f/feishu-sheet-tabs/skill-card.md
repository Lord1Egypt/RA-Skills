## Description:

Creates and organizes worksheet tabs inside an existing Feishu sheet by using browser automation when the normal feishu_sheet API cannot create new worksheet tabs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[g-hanasq](https://clawhub.ai/user/g-hanasq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill when they need an agent to split an existing Feishu spreadsheet into multiple worksheet tabs, then return to structured Feishu sheet writes after tab IDs are known.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify live Feishu spreadsheets through an authenticated browser session.

Mitigation: Use it only with the intended spreadsheet open, require the agent to state the exact create or rename operations, and approve those operations before execution.

Risk: The artifact includes a real-looking example spreadsheet token.

Mitigation: Replace example spreadsheet locators with clearly fake placeholders before publishing or sharing derived instructions.

Risk: Browser automation may target the wrong tab or use an unexpected login state.

Mitigation: Prefer an explicitly attached Browser Relay tab and confirm the active spreadsheet URL before mutating tabs.

## Reference(s):

- [Runtime Notes: Feishu Sheets tab creation](references/runtime-notes.md)
- [ClawHub skill page](https://clawhub.ai/g-hanasq/skills/feishu-sheet-tabs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown status report with browser-evaluation snippets, tab names, tab IDs, login or relay status, and data-fill status]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Feishu worksheet IDs discovered at runtime; users should approve the exact tabs to create or rename before live spreadsheet changes.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
