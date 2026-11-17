## Description:

Run Google Lens or reverse-image search from an image, not for text-only Google Images queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to turn an image URL into a Google Lens or reverse-image-search request through Dataify and receive concise result links and fields.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image URLs and selected search parameters are sent to Dataify for processing.

Mitigation: Use only image URLs appropriate for third-party processing and avoid private or signed image URLs unless necessary.

Risk: A Dataify API token is required for live requests.

Mitigation: Configure the token through DATAIFY_API_TOKEN or a secret manager and avoid passing it with --token where command history or process listings may expose it.

Risk: API calls may consume Dataify account credits.

Mitigation: Use preview or dry-run behavior to review parameters before execution and monitor account credits during repeated use.

## Reference(s):

- [Dataify Google Lens API Reference](artifact/references/google_lens_api.md)
- [Dataify Scraper API endpoint](https://scraperapi.dataify.com/request)
- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-google-lens)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with optional inline shell commands; raw JSON or HTML only when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an image URL and Dataify API token for live requests; previews omit credentials.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
