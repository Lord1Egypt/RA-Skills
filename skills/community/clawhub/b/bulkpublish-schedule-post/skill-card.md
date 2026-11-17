## Description:

Create, schedule, or publish social media posts via BulkPublish MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[azeemkafridi](https://clawhub.ai/user/azeemkafridi)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers and teams use this skill to draft, schedule, publish, and manage approval of posts across connected accounts, including RSS-based posting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A post scheduled for now or the past, or published directly, can become public immediately.

Mitigation: Confirm the destination accounts, content, and time before publishing or scheduling; check whether the response is awaiting approval.

Risk: Retrying an uncertain publication can duplicate a post already live on a platform.

Mitigation: Check the platform account before republishing an unconfirmed post.

Risk: RSS publish mode can create ongoing automatic public posts.

Mitigation: Review the feed, channels, and publish mode before enabling automatic posting; use draft mode for review.

## Reference(s):

- [BulkPublish: Schedule Post on ClawHub](https://clawhub.ai/azeemkafridi/skills/bulkpublish-schedule-post)

## Skill Output:

**Output Type(s):** [Guidance, API calls]

**Output Format:** [Text and structured post or feed requests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create drafts, schedule or publish posts, and configure RSS feeds through connected BulkPublish accounts.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
