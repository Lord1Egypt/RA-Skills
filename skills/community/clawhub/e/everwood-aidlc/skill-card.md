## Description:

Strict human-gated AIDLC planning for non-trivial software work, with per-gate deconfliction review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlwood-dev](https://clawhub.ai/user/mlwood-dev)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to run a human-approved AIDLC planning process for non-trivial OpenClaw software work before implementation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gate-lock helper can persist any readable local text file as a gate artifact when invoked with an unsafe artifact path.

Mitigation: Invoke gate-lock only with gate files inside the active aidlc-sessions/<uuid>/gates directory, and consider patching the helper to reject paths outside the current session.

Risk: Gate artifacts are persistent local planning records and may expose sensitive content if users include secrets or customer data.

Mitigation: Do not put secrets, credentials, tokens, or sensitive customer data in gate artifacts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mlwood-dev/skills/everwood-aidlc)
- [AIDLC Core Workflow](references/core-workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown gate artifacts, deconfliction summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local planning state under aidlc-sessions/<uuid>/ when activated.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
