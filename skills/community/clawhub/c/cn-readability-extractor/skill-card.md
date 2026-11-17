## Description:

Extracts clean article-like text, titles, and descriptions from a supplied webpage URL while removing ads, navigation, scripts, and common page chrome.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to fetch public webpages and convert their HTML into readable Chinese or English text for summarization, analysis, or downstream writing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The URL fetcher can access local files or internal services reachable from the machine running it.

Mitigation: Use the skill only with trusted public HTTP(S) URLs, and avoid internal, authenticated, localhost, metadata-service, and file:// URLs unless that access is explicitly intended and controlled.

Risk: Large or redirected responses can increase exposure when fetching untrusted URLs.

Mitigation: Prefer a safer wrapper that restricts URL schemes to HTTP(S), blocks private and local destinations, validates redirects, and caps response size while streaming.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freedompixels/skills/cn-readability-extractor)
- [AISoBrand Website](https://aisobrand.com)

## Skill Output:

**Output Type(s):** [text, shell commands]

**Output Format:** [Plain text printed to stdout, including title, source URL, optional description, extracted content, and word count.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Extracted content is truncated to 5,000 characters by the bundled script.]

## Skill Version(s):

1.3.2 (source: server release evidence; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
