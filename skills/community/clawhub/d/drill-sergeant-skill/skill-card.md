## Description: <br>
Enforce team communication discipline and execution hygiene in shared work channels by detecting repeat messages, routing errors, missing ownership, stale reviews, and noisy updates, then producing corrective actions, escalation notes, and manager-ready summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ptaramona](https://clawhub.ai/user/ptaramona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineering leads, and agent-operations teams use this skill to review approved team message and task signals, identify communication-discipline issues, and draft concise corrective actions or leadership summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may draft corrective pings or leadership summaries that affect assignments and team perceptions. <br>
Mitigation: Review corrective messages and summaries before sending, and decide in advance whether the skill may post directly or only draft messages. <br>
Risk: Reviewing broad team channels or task sources may expose sensitive operational details. <br>
Mitigation: Limit the review scope, approved sources, and review window before use; keep public-ready outputs free of personal identifiers, secrets, private endpoints, and internal infrastructure details. <br>


## Reference(s): <br>
- [Enforcement Checklist](artifact/references/enforcement-checklist.md) <br>
- [Message Templates](artifact/references/message-templates.md) <br>
- [Public Safety Checklist](artifact/references/public-safety-checklist.md) <br>
- [ClawStation](https://clawstation.dev) <br>
- [ClawHub Skill Listing](https://clawhub.ai/ptaramona/drill-sergeant-skill) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance] <br>
**Output Format:** [Markdown with structured findings, action lists, escalation notes, and all-clear summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each finding includes type, severity, evidence, action, and owner; outputs should avoid secrets, personal identifiers, private endpoints, and webhook URLs.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
