## Description: <br>
Describe a team or organization in plain text and get a complete CellOS-compatible YAML schema with steward roles, scope boundaries, escalation rules, and coordination protocols. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[filipbl4gojevic](https://clawhub.ai/user/filipbl4gojevic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Organizational designers, operators, and developers use this skill to convert plain-text descriptions of teams or initiatives into CellOS cell schemas for governance planning. It is useful when defining steward coverage, scope, escalation paths, coordination protocols, and review notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use may expose internal team structure, roles, escalation paths, and governance details to the agent. <br>
Mitigation: Avoid sharing sensitive organizational details unless the agent environment is approved for that data. <br>
Risk: Generated schemas may be incomplete or unsuitable if treated as adopted policy without review. <br>
Mitigation: Review steward assignments, access, escalation, compliance, and scope sections before adopting the schema. <br>


## Reference(s): <br>
- [CellOS Framework Overview](references/cellos-overview.md) <br>
- [Cell Schema Generator on ClawHub](https://clawhub.ai/filipbl4gojevic/cell-schema-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown containing YAML schema blocks and design notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated schemas should be reviewed before use as organizational policy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
