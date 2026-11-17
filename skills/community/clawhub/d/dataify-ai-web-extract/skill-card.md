## Description:

Trigger when the user needs to extract Markdown, raw HTML, clean HTML, or links from a specified public webpage while controlling content filtering, timeout, and wait conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to extract selected content or links from a public webpage into a chosen format, with optional controls for content filtering and page-load behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requests share the selected URL and supplied headers with the gateway; dry-run output may display supplied headers.

Mitigation: Keep the API token private, use a trusted HTTPS gateway, and avoid sensitive target headers.

## Reference(s):

- [AI Web Extract ClawHub Page](https://clawhub.ai/dataify-server/skills/dataify-ai-web-extract)
- [AI Web API Extract Reference](artifact/references/extract-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML, Links]

**Output Format:** [The selected webpage content or links, returned in a response object.]

**Output Parameters:** [1D — one public webpage, with optional extraction and filtering settings.]

**Other Properties Related to Output:** [Formats include Markdown, raw HTML, clean HTML, or links; options can control main content, tags, headers, cache age, timeout, wait time, and country.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
