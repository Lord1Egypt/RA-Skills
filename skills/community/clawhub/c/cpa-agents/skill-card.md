## Description:

Coordinates OpenClaw agent tasks with parallel runs, branch-fix loops, model comparisons, retries, fallbacks, rollback workflows, and session status tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jose-compu](https://clawhub.ai/user/jose-compu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using OpenClaw can coordinate concurrent agent tasks, compare responses from selected models, recover from failures, and inspect the current session's workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Branch-fix and rollback workflows can modify the current workspace.

Mitigation: Require explicit user approval for repository changes, show planned steps, and keep edits in the current workspace.

Risk: Model fan-out sends task text to every selected model provider.

Mitigation: Require the user to name the models and exclude secrets and private file contents from the task text.

Risk: Installing an unpinned dependency can run unreviewed package code.

Mitigation: Install cpa-agents@0.4.0 with the stated integrity check and use the committed lockfile for reproducible installs.

## Reference(s):

- [Cpa Agents on ClawHub](https://clawhub.ai/jose-compu/skills/cpa-agents)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Agent responses and structured workflow results; session trees can be displayed as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may include traces and session trees.]

## Skill Version(s):

2.1.0 (source: server-resolved release metadata and skill document)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
