## Description:

Publishes content once and syncs it across WordPress, Substack, Medium, and LinkedIn for multi-channel publishing and editorial workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketing teams, newsletter publishers, and B2B teams use this skill to distribute, transform, schedule, and track content across connected publishing platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may help publish, schedule, or bulk sync content across connected platforms.

Mitigation: Confirm every publish, schedule, and bulk sync before execution, especially when multiple platforms or delayed distribution are involved.

Risk: Platform tokens, Slack webhooks, and Google Drive service-account access can expose content beyond the original platform if they are broad or mishandled.

Mitigation: Use scoped platform tokens where possible, store credentials in the approved secret store, and avoid logging or sharing credential values.

Risk: Cross-platform transformations can change formatting, metadata, calls to action, or audience framing.

Mitigation: Review transformed drafts, target platforms, metadata, and canonical URL settings before final publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ncreighton/skills/cross-platform-content-syncer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with status summaries, reports, configuration snippets, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include publish confirmations, platform-specific transformation summaries, scheduling details, analytics reports, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
