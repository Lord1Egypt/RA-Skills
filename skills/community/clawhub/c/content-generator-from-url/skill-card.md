## Description:

All-in-one content generation, social media publishing, video creation, and image template design via the GenerateBot API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[osaket](https://clawhub.ai/user/osaket)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to search for content ideas, generate articles and social posts from URLs or topics, create short-form videos, render image templates, and publish to connected CMS or social media accounts through GenerateBot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing and scheduling can act through connected social or CMS accounts.

Mitigation: Require explicit user confirmation that names the destination platform, account, content item, and schedule before making publishing or scheduling API calls.

Risk: Content deletion, RSS clearing, and template deletion can remove saved account data.

Mitigation: Require explicit confirmation of the exact resource ID or feed set before destructive API calls, and show the target back to the user before proceeding.

Risk: Pipeline, video, image, enrichment, and template-render operations may spend GenerateBot credits.

Mitigation: State the expected credit cost and get user confirmation before starting credit-consuming workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/osaket/skills/content-generator-from-url)
- [Publisher profile](https://clawhub.ai/user/osaket)
- [GenerateBot homepage](https://generatebot.com)
- [GenerateBot API base URL](https://generatebot.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON request and response examples, API endpoint references, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GENERATEBOT_API_KEY bearer token; some workflows consume GenerateBot credits and may operate on connected social or CMS accounts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
