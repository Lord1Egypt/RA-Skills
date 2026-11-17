## Description:

Review your Extrovert campaigns and LinkedIn comment queue. Read-only API access; prepare edits and recommendations for a human to apply. Requires a paid Extrovert account and API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olegantor](https://clawhub.ai/user/olegantor)

### License/Terms of Use:

MIT-0

## Use Case:

External Extrovert account owners use this skill to review their authorized campaigns' LinkedIn comment queues, compare drafts with source posts, and prepare recommendations for a human to apply in Extrovert.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private campaign, post, and draft content could be exposed through shared logs or conversations.

Mitigation: Keep review output within the user's authorized chat and out of shared logs; store the API key in secret settings.

Risk: A user could review a campaign they are not authorized to access.

Mitigation: Review only the user's own campaign or one they explicitly authorize, and confirm the publishing owner when ambiguous.

Risk: Recommendations could be mistaken for approved or published changes.

Mitigation: Treat recommendations as drafts for a human to confirm and apply in Extrovert; the skill does not approve, edit, or publish.

## Reference(s):

- [Extrovert](https://goextrovert.com/)
- [Extrovert integrations and API key settings](https://app.goextrovert.com/dashboard/settings/integrations)
- [Extrovert API documentation](https://api-docs.goextrovert.com/)
- [Extrovert OpenAPI schema](https://api.goextrovert.com/client/v2/docs-json)
- [ClawHub skill page](https://clawhub.ai/olegantor/skills/extrovert-comment-review)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Markdown]

**Output Format:** [Markdown review with source post links, queue state, draft assessment, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are for human review; the skill makes no campaign or publishing changes. Review output may contain private campaign, post, and draft content.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
