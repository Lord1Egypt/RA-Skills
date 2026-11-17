## Description:

Finds food content creators across Instagram, TikTok, and YouTube using apidojo's social media scrapers on Apify, returning creator handles, platform metrics, engagement signals, content themes, and post samples for campaign outreach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, agency, and campaign teams use this skill to discover and evaluate food bloggers, recipe creators, restaurant reviewers, and food content creators for partnerships and outreach. It helps segment creators by platform, niche, engagement quality, and cross-platform presence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Apify API tokens may be exposed when passed in URL query strings used by example commands.

Mitigation: Prefer Apify MCP or API calls that send APIFY_TOKEN in an Authorization header, and use narrowly scoped tokens.

Risk: Scraped creator data may be written to local CSV or JSON outputs without the user's full awareness.

Mitigation: Confirm the output path, file format, and data handling expectations before saving creator lists.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apidojo-io/skills/finding-food-bloggers-and-creators)
- [API Dojo publisher profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown creator lists with tables, optional shell commands, and optional CSV or JSON file output guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an APIFY_TOKEN environment variable and can use Apify MCP when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
