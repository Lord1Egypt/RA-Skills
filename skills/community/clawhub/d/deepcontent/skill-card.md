## Description:

DeepContent supports recipe lookup, content generation, and asset management for event templates, speaker cards, partnership posts, social media generation, and event posters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thierrypdamiba](https://clawhub.ai/user/thierrypdamiba)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use DeepContent to list DeepContent recipes and generate branded social media content such as event posters, speaker announcement cards, and LinkedIn partnership posts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may search public websites for templates, logos, or headshots when users do not provide approved asset URLs.

Mitigation: Prefer user-provided approved asset URLs and review any discovered images, logos, or headshots before publishing generated content.

Risk: Image recipes require publicly accessible input URLs, which can expose unintended assets if private or sensitive links are supplied.

Mitigation: Use only public, publication-approved assets and avoid providing private, sensitive, or access-controlled URLs.

## Reference(s):

- [DeepContent ClawHub Skill Page](https://clawhub.ai/thierrypdamiba/skills/deepcontent)

## Skill Output:

**Output Type(s):** [Text, Images, API Calls, Guidance]

**Output Format:** [MCP tool responses with text blocks, image URLs, status, recipe ID, and generation ID]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image recipes may take 2-3 minutes and require publicly accessible template, logo, or headshot URLs.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
