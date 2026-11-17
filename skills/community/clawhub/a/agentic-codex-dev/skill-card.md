## Description:

Review agentic software-development plans and release readiness for Codex, GitHub, and ClawHub work. Use when a user asks for scoped delivery planning, implementation review, public-surface checks, or release evidence review without running remote-changing commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release reviewers use this skill to review Codex, GitHub, and ClawHub delivery plans, diffs, release checklists, public-facing wording, verification evidence, and readiness before publication or remote-changing work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Readiness verdicts may be mistaken for authorization to publish, push, or run account-changing commands.

Mitigation: Treat verdicts as advisory and require normal human approval, test gates, and release controls before remote-changing actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zack-dev-cm/skills/agentic-codex-dev)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown sections with findings, public-surface review, verification checks, and a readiness verdict]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdict is one of ready, ready_with_notes, blocked, or do_not_ship.]

## Skill Version(s):

0.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
