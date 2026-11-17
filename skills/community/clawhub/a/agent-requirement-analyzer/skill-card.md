## Description:

Analyzes AI agent platform requirements documents to extract test requirements, functional areas, interaction scenarios, boundary conditions, and open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luiciferyi](https://clawhub.ai/user/luiciferyi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers, product reviewers, and agent platform teams use this skill to turn PRDs or user stories into a structured requirements analysis report with functional modules, test focus areas, interaction scenarios, boundary conditions, and items needing confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can write PRD-derived requirements analysis to a fixed external Feishu destination without clear user confirmation or destination control.

Mitigation: Use it only when the Feishu destination is trusted; for confidential PRDs, require preview and approval before writing or remove Feishu write and update permissions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luiciferyi/skills/agent-requirement-analyzer)
- [Publisher profile](https://clawhub.ai/user/luiciferyi)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown requirements analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include tables, Mermaid diagrams, and a list of unclear, missing, or conflicting requirements needing confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
