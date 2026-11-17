## Description:

AI content marketing pipeline that generates branded LinkedIn, X, and Reddit posts from any URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, founders, and content operators use this skill to turn URLs into branded social posts, discover content topics, manage brands, and route users to DeepContent account workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a DeepContent API key and sends URLs plus brand or account context to DeepContent.

Mitigation: Install only for accounts that approve this data flow, and avoid URLs or business data that should not be processed by DeepContent.

Risk: Generated posts, brand confirmations, and team invites may affect public content or account access if approved without review.

Mitigation: Review generated posts, brand confirmations, and team invites before approval.

Risk: Security evidence flags broad triggers and persistent preference memory as under-scoped.

Mitigation: Use the skill deliberately for DeepContent workflows and periodically review remembered platform, brand, and edit preferences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/thierrypdamiba/skills/deepcontentskill23223)
- [DeepContent App Homepage](https://deepcontent-frontend.scaleintelligence.workers.dev)
- [DeepContent OpenAPI Spec](https://deepcontent-api.scaleintelligence.workers.dev/api/docs/openapi.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Markdown responses with social post drafts, dashboard links, account status, and concise workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires DEEPCONTENT_API_KEY for authenticated DeepContent workflows.]

## Skill Version(s):

2.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
