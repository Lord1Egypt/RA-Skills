## Description:

Organize and store digital assets across cloud providers with automated workflows for DAM integration, file organization, and asset metadata management for creative teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ncreighton](https://clawhub.ai/user/ncreighton)

### License/Terms of Use:

MIT-0

## Use Case:

Creative operations teams and developers use Assetflow to organize, tag, sync, archive, and report on digital assets across cloud storage, DAM systems, Slack, and Google Sheets. It is intended for workflows that need structured asset taxonomies, metadata templates, retention rules, and review queues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad cloud storage and DAM access could move, tag, index, share, or notify on more assets than intended.

Mitigation: Run a dry run first, narrow target folders or buckets, and require confirmation before write or archive actions.

Risk: Asset metadata, previews, OCR results, or AI-derived analysis may expose sensitive repository content through Slack or third-party providers.

Mitigation: Disable OCR or AI analysis for sensitive repositories unless explicitly needed, and review metadata or preview payloads before sending them to notification channels or external services.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ncreighton/skills/assetflow)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with configuration examples, shell commands, workflow guidance, and status/report examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce asset organization reports, sync status summaries, search results, setup instructions, taxonomy examples, and troubleshooting steps.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
