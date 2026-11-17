## Description:

Reviews CloudKit code for container setup, record handling, subscriptions, and sharing patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Swift CloudKit integrations for common correctness, deployment, synchronization, sharing, and error-handling issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on an unbundled sibling review-verification-protocol file that can affect whether findings are reported.

Mitigation: Install only when that protocol is trusted, bundled with the release, or pinned to a reviewed version.

Risk: Review findings may be changed or suppressed if the external protocol changes without visibility.

Mitigation: Review the protocol alongside this skill before relying on the skill for CloudKit code-review decisions.

## Reference(s):

- [CloudKit Container Setup](references/container-setup.md)
- [CloudKit Records](references/records.md)
- [CloudKit Sharing](references/sharing.md)
- [CloudKit Subscriptions](references/subscriptions.md)
- [ClawHub Skill Page](https://clawhub.ai/anderskev/skills/cloudkit-code-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown issue reports using [FILE:LINE] ISSUE_TITLE entries, review questions, and concise supporting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are expected to satisfy location, scope, CloudKit artifact, and review protocol gates before reporting.]

## Skill Version(s):

1.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
