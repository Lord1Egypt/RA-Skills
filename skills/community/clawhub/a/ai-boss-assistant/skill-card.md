## Description:

AI Boss Assistant provides persona and workflow templates for training an AI agent as an executive assistant with Google Workspace workflows, staged delivery, and security guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacky6658](https://clawhub.ai/user/jacky6658)

### License/Terms of Use:

MIT

## Use Case:

Solo entrepreneurs, small team founders, busy professionals, and AI builders use this skill to configure an AI agent for executive-assistant work such as schedule management, email handling, document workflows, task tracking, and staged project delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup can grant broad Google Workspace access for Gmail, Calendar, Drive, Docs, and Sheets.

Mitigation: Use the minimum OAuth scopes needed for the deployment, keep account authorizations separated by purpose, review granted services, and revoke unused tokens.

Risk: OAuth credentials, Telegram bot tokens, API keys, or local token files could be exposed through configuration files, backups, or Git history.

Mitigation: Store secrets in environment or gateway configuration, protect local credential paths, create a .gitignore before committing, and require explicit confirmation before any push or public action.

Risk: Browser automation and assistant autonomy could perform sensitive external actions such as form submission, messaging, booking, or payment steps.

Mitigation: Stop at confirmation pages for bookings or payments, require human approval for sensitive external actions, and avoid automation where site terms or anti-bot controls make it inappropriate.

Risk: Installation and gateway setup instructions include global package installs, pipe-to-shell commands, service configuration, and optional communication channels.

Mitigation: Review package identities and setup commands before running them, avoid unpinned or pipe-to-shell installs where possible, and disable gateway, admin, camera, or messaging capabilities unless intentionally needed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jacky6658/skills/ai-boss-assistant)
- [Project repository](https://github.com/jacky6658/ai-boss-assistant)
- [OpenClaw](https://openclaw.ai)
- [gog Google Workspace CLI](https://github.com/steipete/gog)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown templates with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces reusable assistant persona, workflow, setup, task, browser automation, and security guidance artifacts.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
