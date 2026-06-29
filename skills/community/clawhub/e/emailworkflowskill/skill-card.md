## Description: <br>
Helps agents plan, review, audit, and improve email workflows focused on workflow maps, lifecycle routing, trigger ownership, and operator-ready paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[polnikale](https://clawhub.ai/user/polnikale) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and email teams use this skill to map lifecycle routes, review trigger logic, find routing collisions, and prepare QA-ready workflow changes before production action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Email workflow recommendations may affect live sends, contact imports, suppression rules, DNS/authentication settings, or production automations if applied without review. <br>
Mitigation: Keep the skill's approval gate in place and require explicit approval before any high-risk live-system action. <br>
Risk: Email audits can involve customer or recipient data that is not necessary for planning. <br>
Mitigation: Do not provide unnecessary customer data; use focused workflow details, examples, and platform exports only when needed for the review. <br>


## Reference(s): <br>
- [Email Workflow Skill Operating Checklist](references/operating-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown workflow maps, trigger inventories, routing diffs, handoff notes, collision audits, and QA plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, suppression changes, DNS/authentication work, or production automation edits.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
