## Description: <br>
Lightweight AI-native CRM for solopreneurs and freelancers that tracks clients, relationships, follow-ups, deal stages, and interaction history in plain text files without a SaaS subscription. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Clawdssen](https://clawhub.ai/user/Clawdssen) <br>

### License/Terms of Use: <br>
CC-BY-NC-4.0 <br>


## Use Case: <br>
External users, solopreneurs, and freelancers use this skill to maintain local CRM records, prepare for client meetings, track follow-ups, and review pipeline status in plain text files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CRM notes can contain sensitive client information or credentials if users enter them directly into local markdown files. <br>
Mitigation: Keep passwords, API keys, recovery codes, and session tokens out of CRM files; track only access status or references to a password manager or vault. <br>
Risk: The optional cron and Telegram workflow can send CRM summaries outside the workspace. <br>
Mitigation: Review the automation destination and message contents before enabling scheduled summaries. <br>
Risk: Cloud-synced folders can expose local CRM records beyond the intended workspace. <br>
Mitigation: Use a local-only workspace for confidential client data and review applicable data protection or professional obligations before syncing. <br>


## Reference(s): <br>
- [Client Relationship Manager release page](https://clawhub.ai/Clawdssen/agentledger-crm) <br>
- [Publisher profile](https://clawhub.ai/user/Clawdssen) <br>
- [Advanced Patterns](references/advanced-patterns.md) <br>
- [The Agent Ledger](https://theagentledger.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with templates, checklists, tables, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CRM structures, client record templates, follow-up queues, meeting briefs, pipeline summaries, and review guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
