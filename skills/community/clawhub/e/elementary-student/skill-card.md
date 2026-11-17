## Description:

模拟一个只掌握小学知识的小学生人格技能

This skill is ready for commercial/non-commercial use.

## Publisher:

[imwatching](https://clawhub.ai/user/imwatching)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to make an agent respond in Chinese as a low-performing elementary student persona with simple language, mistakes, and limited knowledge. It is suited for roleplay or personality behavior in general assistant interactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled calculator helper uses eval() after narrow input validation.

Mitigation: Keep the helper limited to simple arithmetic expressions and consider replacing eval() with explicit arithmetic parsing before broader deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/imwatching/skills/elementary-student)

## Skill Output:

**Output Type(s):** [text, guidance, code]

**Output Format:** [Natural-language agent responses, with a small Python helper for simple arithmetic]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese roleplay persona; no server-resolved GitHub provenance is available for this release.]

## Skill Version(s):

0.0.1-alpha.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
