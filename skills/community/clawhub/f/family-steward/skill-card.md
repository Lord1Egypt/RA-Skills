## Description: <br>
AI-powered family office management system for ultra-high-net-worth families - manage family members, professional contacts, legal documents, and tasks with natural language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZhenStaff](https://clawhub.ai/user/ZhenStaff) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and family-office teams use this skill to manage family member records, professional contacts, legal and financial document tracking, task coordination, and dashboard-style reminders through an agent interface. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is intended for highly sensitive family, contact, legal-document, health-note, and task metadata. <br>
Mitigation: Verify storage location, encryption behavior, backup exposure, export, and deletion workflows before entering real data. <br>
Risk: Broad activation language could cause the agent to surface or organize sensitive records during loosely related requests. <br>
Mitigation: Confirm the user's intent and scope before retrieving or summarizing sensitive family-office information. <br>
Risk: The included publishing helper runs shell commands and accepts user-controlled arguments. <br>
Mitigation: Review commands before execution and do not run the publishing helper with untrusted arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZhenStaff/family-steward) <br>
- [NPM package](https://www.npmjs.com/package/openclaw-family-steward) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with structured lists, summaries, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize sensitive family-office records, deadlines, contacts, and document status when the local data source is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, CHANGELOG released 2026-03-08, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
