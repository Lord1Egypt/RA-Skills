## Description:

agpair helps an AI coding agent delegate coding work to Antigravity through the agpair CLI, including preflight checks, task dispatch, waiting, evidence review, and follow-up actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[logicrw](https://clawhub.ai/user/logicrw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding-agent operators use this skill when an AI agent controls delegated Antigravity execution. It guides the agent through health checks, task dispatch or monitoring, evidence review, and continue, approve, reject, or retry decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad delegation phrases may trigger the agpair workflow when the user did not intend to delegate work to Antigravity.

Mitigation: Invoke the skill only for intentional agpair or Antigravity delegation requests, and confirm task status and logs before continuing work.

Risk: Delegated coding work may be incomplete, stale, or unsuitable for approval without reviewer judgment.

Mitigation: Review health checks, current task status, latest logs, and any evidence pack before approving, rejecting, continuing, or retrying a task.

## Reference(s):

- [ClawHub agpair skill page](https://clawhub.ai/logicrw/skills/agpair)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local agpair CLI and Antigravity task state where the guided workflow is invoked.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
