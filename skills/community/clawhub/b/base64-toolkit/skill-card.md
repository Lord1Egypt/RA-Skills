## Description:

Base64 encoding and decoding toolkit. Encode/decode text, URL-safe Base64, and image to Base64 conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freeter226](https://clawhub.ai/user/freeter226)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to encode and decode Base64 text, generate URL-safe Base64 strings, and convert intended image files into Base64 data URIs for API authentication, data transmission, URL parameters, and embedding workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The image conversion command can expose readable local files because it does not verify that the input path is an intended image.

Mitigation: Use image-encode and --file only with reviewed, non-sensitive paths; avoid keys, tokens, configuration files, and private documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freeter226/skills/base64-toolkit)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled Python utility prints JSON results for encode, decode, URL-safe encode/decode, and image-to-data-URI actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
