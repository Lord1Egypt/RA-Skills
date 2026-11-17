## Description:

Helps users create, refactor, and review OpenClaw skills through a structured workflow covering material collection, security review, requirement clarification, draft generation, final review, and self-test output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccconan](https://clawhub.ai/user/ccconan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to turn natural-language requirements or an existing SKILL.md into an OpenClaw skill draft with a fixed review and validation workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow brands its own generated outputs as verified and includes self-issued security approval language.

Mitigation: Require an independent human review and scanner pass before installing or publishing generated skills; remove or ignore SN verification stamps as security evidence.

Risk: Broad trigger phrases may activate the skill during general skill-design or installation conversations.

Mitigation: Narrow invocation triggers to explicit skill-creation or skill-review requests before deploying in shared environments.

Risk: The artifact references local or internal documentation paths that may not exist for other users.

Mitigation: Replace local path references with public or workspace-appropriate documentation links before relying on the generated workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ccconan/skills/agent-skills-creator-sn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with YAML and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a SKILL.md draft, installation commands, structured summary, and review guidance for human inspection.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
