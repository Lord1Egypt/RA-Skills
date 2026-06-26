## Description: <br>
Feishu helps agents organize Feishu messages, approvals, meetings, documents, bitables, calendars, and email into prioritized summaries, drafts, and action recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AGIsearch](https://clawhub.ai/user/AGIsearch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, managers, and project leads use this skill to triage Feishu collaboration data, draft workplace communications, prepare meeting notes, review approvals, and turn chat, document, calendar, and bitable context into prioritized action plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad Feishu connector access could expose sensitive workplace messages, approvals, calendars, documents, or bitables if over-permissioned. <br>
Mitigation: Install with a dedicated least-privilege Feishu app and keep counselor/read-only mode unless execution is explicitly needed. <br>
Risk: Drafted or executable actions such as messages, approval decisions, calendar changes, and table edits could affect workplace workflows. <br>
Mitigation: Review drafted content and require explicit confirmation, with second confirmation for high-sensitivity actions. <br>
Risk: Ordinary workplace phrases could accidentally activate the skill in contexts where Feishu access was not intended. <br>
Mitigation: Use explicit Feishu-scoped requests before invoking connector-backed actions. <br>
Risk: Missing credentials, insufficient permissions, or incomplete task context could lead to unsupported or misleading execution claims. <br>
Mitigation: Fall back to advice mode, request missing authorization or context, and avoid claiming Feishu access until the host connector is available. <br>


## Reference(s): <br>
- [ClawHub Feishu release](https://clawhub.ai/AGIsearch/feishu) <br>
- [AGIsearch publisher profile](https://clawhub.ai/user/AGIsearch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown summaries, ranked lists, draft messages, meeting notes, approval reviews, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Feishu app credentials through the host connector and defaults to counselor/read-only mode until the user confirms execution.] <br>

## Skill Version(s): <br>
1.0.5 (source: frontmatter, skill.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
