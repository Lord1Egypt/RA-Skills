## Description:

Permanent OpenClaw meta-skill for routing, creating, auditing, and self-evolving skills through an iterative generator-verifier loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[147258xuan](https://clawhub.ai/user/147258xuan)

### License/Terms of Use:

MIT

## Use Case:

Developers and skill maintainers use OpenClaw EvoSkills to audit and iteratively improve existing agent skills, create skills from repeated workflows, and configure an OpenClaw workspace to observe those workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activating the skill can make persistent changes to workspace instructions and OpenClaw configuration, affecting later sessions.

Mitigation: Review the activation script and proposed file and configuration changes before running it; keep a backup of affected workspace and OpenClaw settings.

Risk: The repetition observer can repeatedly inspect memory and session traces, which may include sensitive information and influence future skill creation.

Mitigation: Review which traces the observer can access and how often it runs; disable the observer or limit its inputs if recurring inspection is not appropriate.

## Reference(s):

- [Evolution Loop](references/evolution-loop.md)
- [Meta-Skill Policy](references/meta-skill-policy.md)
- [Hermes Alignment Notes](references/hermes-alignment.md)
- [ClawHub Skill Listing](https://clawhub.ai/147258xuan/skills/evoskills-master)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance, edited skill files, shell command examples, and structured verification reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the target skill, requested improvement, and verification results.]

## Skill Version(s):

0.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
