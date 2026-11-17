## Description:

Design data models for construction projects. Create entity-relationship diagrams, define schemas, and generate database structures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and construction technology teams use this skill to define construction project entities, relationships, SQL schemas, JSON Schemas, and Mermaid ER diagrams from project data requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The AI suggestion feature can send project descriptions to SkillBoss API Hub.

Mitigation: Use local schema and ERD features for sensitive work, and only use AI suggestions with non-confidential data after approving SkillBoss API Hub data-handling terms.

Risk: The artifact metadata declares filesystem permission but not network permission while the AI suggestion feature calls an external API.

Mitigation: Review permissions and external data flow before installation or deployment.

## Reference(s):

- [Data Driven Construction](https://datadrivenconstruction.io)
- [SkillBoss API Hub endpoint](https://api.heybossai.com/v1/pilot)
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/abe-data-model-designer)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Structured Markdown with generated SQL DDL, JSON Schema, Mermaid ER diagram text, validation findings, and export guidance when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call SkillBoss API Hub for AI-assisted entity suggestions when SKILLBOSS_API_KEY is configured.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
