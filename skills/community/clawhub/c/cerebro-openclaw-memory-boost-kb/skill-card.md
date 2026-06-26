## Description: <br>
Enforces a Cerebro-first operating protocol by having an agent identify the work domain, read authoritative Cerebro docs and recent memory logs, cite its decision basis, and write durable updates back to local knowledge files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ptaramona](https://clawhub.ai/user/ptaramona) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use this skill to make an agent preserve project continuity across sessions, route operational tasks to the right local Cerebro documents, and produce traceable completion updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause an agent to read private Cerebro and memory notes as a durable source of truth. <br>
Mitigation: Review the Cerebro and memory folders before use, keep secrets out of those notes, and restrict the skill to intended workspaces. <br>
Risk: The skill can cause an agent to create or update persistent operational records without consistently requiring user approval. <br>
Mitigation: Require the agent to show exact write-back paths and proposed file content before creating or updating files. <br>
Risk: Domain routing may involve private company or project contexts. <br>
Mitigation: Verify the selected domain before sharing outputs, and keep private contexts in private owner or admin channels. <br>


## Reference(s): <br>
- [Cerebro Index v2.1](references/cerebro-index-v2.1.md) <br>
- [Domain Routing v2.1](references/domain-routing-v2.1.md) <br>
- [Startup Checklist](references/startup-checklist.md) <br>
- [Scenario Profiles v2.1](references/scenario-profiles-v2.1.md) <br>
- [Enforcement Checklist v2.1](references/enforcement-checklist-v2.1.md) <br>
- [Done Schema v2.1](references/done-schema-v2.1.md) <br>
- [Decision Log Template](references/decision-log-template.md) <br>
- [Missing Doc Bootstrap Template](references/missing-doc-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown with structured status sections and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or update local Cerebro documentation and daily memory files when workflow rules change.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact docs describe Cerebro protocol v2.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
