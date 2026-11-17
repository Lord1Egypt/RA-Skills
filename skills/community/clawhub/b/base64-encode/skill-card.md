## Description:

Encode or decode text using Base64, URL percent-encoding, or HTML entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ohernandez-dev-blossom](https://clawhub.ai/user/ohernandez-dev-blossom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to transform text between Base64, URL percent-encoding, and HTML entity representations, or to reverse those transformations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad requests to encode or decode text may trigger this skill when the user intended a different transformation.

Mitigation: Confirm the requested encoding type and direction before transforming ambiguous input.

Risk: Binary data cannot be faithfully processed when only plain text is available.

Mitigation: Use this skill for text input, and use a byte-aware file tool when raw binary content must be encoded or decoded.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Plain text or Markdown containing the transformed string and a brief note]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports type options base64, url, and html, and direction options encode and decode.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
