## Description:

Temporary skill that documents a realistic owner migration validation workflow.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[openclaw](https://clawhub.ai/user/openclaw)

### License/Terms of Use:

MIT-0

## Use Case:

ClawHub maintainers use this skill to validate the owner migration flow for a disposable skill record, including publishing, owner transfer with explicit opt-in, inspection, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the owner migration steps to a real production skill could unintentionally transfer ownership or remove a skill during cleanup.

Mitigation: Use the workflow only for maintainer validation with a disposable skill record, and confirm that any ownership change and cleanup are intentional before running the steps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openclaw/skills/codex-owner-move-1778257136)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown checklist guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No automatic behavior; the artifact provides maintainer-facing validation steps.]

## Skill Version(s):

0.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
