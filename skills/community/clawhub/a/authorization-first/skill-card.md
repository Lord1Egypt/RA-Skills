## Description:

Authorization First guides agents to explain intended file, system, configuration, or external operations and wait for explicit user authorization before taking action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikaqiuyaya](https://clawhub.ai/user/pikaqiuyaya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to make assistants request explicit approval before file changes, state-changing commands, configuration edits, or external service calls. It provides reusable templates for stating intent, showing planned changes, describing impact and risk, waiting for confirmation, and reporting errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Non-Chinese users may misunderstand the operational templates because the artifact text is written in Chinese.

Mitigation: Review and localize the templates before deployment in non-Chinese operating environments.

Risk: Approval-first behavior can slow urgent changes if teams have not defined what the agent may do without asking.

Mitigation: Document local approval boundaries, including read-only actions and emergency procedures, before relying on the skill in operational workflows.

## Reference(s):

- [Authorization First on ClawHub](https://clawhub.ai/pikaqiuyaya/skills/authorization-first)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with approval templates and inline command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language operational templates; no executable code.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
