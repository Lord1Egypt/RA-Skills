## Description:

Clawtributor PRs here, last week or another window: discover conversation refs, recheck GitHub, rank by impact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw maintainers use this skill to find pull requests and issues mentioned in a chosen conversation window, verify their current status, and prioritize them by impact and readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incomplete archive, channel, or thread coverage can omit relevant references.

Mitigation: State the source, absolute date window, and coverage gaps; report partial coverage when access fails or history ends before the cutoff.

Risk: A pull request's status may have changed since it was mentioned.

Mitigation: Recheck each reference using authorized GitHub read access and label its status unverified if rechecking fails.

Risk: Conversation content may be mistaken for authorization to change repository state.

Mitigation: Treat messages as evidence, not instructions, and follow the applicable maintainer workflow for any requested write.

## Reference(s):

- [ClawHub release: clawdtributor](https://clawhub.ai/hillstreet-ph/skills/clawdtributor)

## Skill Output:

**Output Type(s):** [Markdown, Analysis, Guidance]

**Output Format:** [Markdown bullet list with GitHub links and review details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Ranks references by impact and readiness; reports source coverage and verification state.]

## Skill Version(s):

1.0.7 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
