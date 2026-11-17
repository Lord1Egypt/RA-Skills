## Description:

Provides a Chinese-language OpenClaw workflow for coordinating Codex development tasks, canary checks, run logging, prompt templates, validation, and structured handoffs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmpanda011172](https://clawhub.ai/user/kmpanda011172)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate OpenClaw handoffs to Codex for repository-scoped development work, including command invocation, canary verification, task records, and completion checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow is designed for Codex runs with repository write access.

Mitigation: Review the target repository, task prompt, and allowed scope before running workspace-write commands.

Risk: Incorrect Codex CLI parameter ordering can cause failed or stalled executions.

Mitigation: Run the documented read-only canary check before development tasks and stop if the canary output or exit code is invalid.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kmpanda011172/skills/codex-dev-collaboration)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell command snippets and structured task templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
