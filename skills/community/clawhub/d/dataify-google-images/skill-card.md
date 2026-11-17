## Description:

Search Google Images for image results, not Google Lens reverse-image search or general web results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn Google Images requests into Dataify Scraper API searches and receive concise image-result links or raw JSON/HTML when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Searches may send the user's query, filters, and location fields to Dataify.

Mitigation: Avoid precise locations or sensitive searches unless the user is comfortable sharing them with the service.

Risk: The skill requires a Dataify API token and consumes Dataify access.

Mitigation: Configure DATAIFY_API_TOKEN through an environment variable, never place tokens in chat, and confirm broad or multi-page searches before spending additional access.

## Reference(s):

- [Dataify Google Images API Reference](artifact/references/google_images_api.md)
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/skills/dataify-google-images)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Concise Markdown summaries by default; raw JSON or HTML when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include source links, result counts, truncation notes, and token setup guidance when needed.]

## Skill Version(s):

1.3.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
