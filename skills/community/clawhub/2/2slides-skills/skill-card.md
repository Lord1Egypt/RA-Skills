## Description:

AI-powered presentation generation using the 2slides API, including slide creation from text, reference image style matching, document summarization, theme search, exports, and voice narration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[javainthinking](https://clawhub.ai/user/javainthinking)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate presentations, PDFs, slide images, and narrated slide assets from supplied text, documents, or reference images through the 2slides service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation text, document-derived content, and reference images are sent to 2slides.

Mitigation: Install only when this data sharing is acceptable for the intended content and audience.

Risk: API keys may be exposed if placed in URLs or shared logs.

Mitigation: Prefer protected secret storage or Authorization headers, avoid putting API keys in URLs, and rotate any key that may have been logged or shared.

Risk: The MCP setup can run an unpinned package.

Mitigation: Prefer the direct Python scripts or a pinned, reviewed MCP package before installation.

## Reference(s):

- [2slides API Reference](references/api-reference.md)
- [2slides MCP Integration Guide](references/mcp-integration.md)
- [2slides Pricing and Credit Information](references/pricing.md)
- [2slides API Access](https://2slides.com/api)
- [2slides Pricing](https://2slides.com/pricing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API responses, presentation URLs, PDF downloads, ZIP archives, PNG slide images, WAV narration files, and transcripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a 2slides API key and may send presentation text, document-derived content, and reference images to 2slides.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
