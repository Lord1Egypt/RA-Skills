## Description:

DeepContent recipe lookup, content generation, and asset management for branded social media content, event posters, speaker cards, partnership posts, and recipe-based generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scale-intelligence](https://clawhub.ai/user/scale-intelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content operators use this skill to list DeepContent recipes, run recipe-based content generation, remix recipes, and return generated image and text blocks for social media or event workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private images, temporary file links, personal headshots, company logos, or client assets may be uploaded to DeepContent and returned as permanent public URLs.

Mitigation: Confirm user consent before upload, avoid private or client-confidential assets unless approved, and verify rights to any online image before use.

Risk: The skill may search for logos or headshots when users do not provide asset URLs, which can introduce incorrect identities or unlicensed imagery.

Mitigation: Verify that discovered assets are direct public HTTPS image URLs, represent the intended person or organization, and are permitted for the intended use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/scale-intelligence/skills/deep-content)
- [DeepContent Recipe UI](https://deepcontent-pair.vercel.app/recipes)

## Skill Output:

**Output Type(s):** [Text, Markdown, Images, URLs, Guidance]

**Output Format:** [Markdown or chat text with generated content blocks and public URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generation responses may include recipe IDs, generation IDs, status values, generated image URLs, captions, and site URLs.]

## Skill Version(s):

1.3.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
