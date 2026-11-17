## Description:

Creates a repeatable daily review workflow across available conversation surfaces, producing per-source raw notes, one merged daily summary, index updates, verification, and an optional management update.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panpansirius-cloud](https://clawhub.ai/user/panpansirius-cloud)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review the last 24 hours of activity across available conversation channels, generate per-channel raw notes, synthesize a cross-channel daily review, maintain an index, and optionally prepare a short management summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local session transcripts and creates persistent daily review memory, which may include sensitive workspace content.

Mitigation: Run it only in workspaces where transcript review is appropriate, restrict input paths to intended session directories, and review generated memory files before sharing.

Risk: Security evidence flags unsafe local file handling and recommends strict path validation.

Mitigation: Require slug/date validation and archive source containment before using the skill on sensitive or multi-user workspaces.

Risk: The daily runner can append promoted review rules to persistent rules.md.

Mitigation: Require explicit approval before accepting generated rules or committing persistent rule changes.

Risk: Boss-summary delivery may fall back to another available destination if the preferred channel is unavailable.

Mitigation: Confirm the final delivery target before any external or cross-channel summary is sent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/panpansirius-cloud/skills/cross-channel-daily-review)
- [Architecture](references/architecture.md)
- [Channel Adapter Spec](references/channel-adapter-spec.md)
- [Delivery Modes](references/delivery-modes.md)
- [Failure Handling](references/failure-handling.md)
- [Known Limitations](references/known-limitations.md)
- [Lifecycle Automation](references/lifecycle-automation.md)
- [Release Readiness](references/release-readiness.md)
- [Review Dimensions](references/review-dimensions.md)
- [Validation Report](references/validation-report.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown review reports, JSON indexes and manifests, and shell command plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes daily-review files under memory/daily-review and verifies generated outputs before reporting success.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
