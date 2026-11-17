## Description:

Extracts web page content from a URL using the Felo Web Extract API, with support for HTML, text, Markdown, readability mode, target selectors, and wait selectors.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangzhiming1999](https://clawhub.ai/user/wangzhiming1999)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to extract readable content from web page URLs for summarization, conversion, capture, or downstream processing. It is suited for webpage-to-Markdown/text workflows and targeted element extraction through CSS selectors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send a Felo API key and requested URLs to an environment-selected API host.

Mitigation: Keep FELO_API_BASE unset unless the destination is trusted, avoid private or tokenized URLs, and protect, scope, and rotate FELO_API_KEY if exposed.

Risk: The optional global npm install path depends on a packaged CLI outside the bundled artifact.

Mitigation: Prefer the bundled script where possible, or verify the exact npm package version and provenance before installing globally.

## Reference(s):

- [Felo Web Extract API](https://openapi.felo.ai/docs/api-reference/v2/web-extract.html)
- [Felo Open Platform](https://openapi.felo.ai/docs/)
- [ClawHub Skill Page](https://clawhub.ai/wangzhiming1999/skills/felo-web-extract)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text, HTML, JSON, shell commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses FELO_API_KEY for authentication; FELO_API_BASE can override the default API host.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
