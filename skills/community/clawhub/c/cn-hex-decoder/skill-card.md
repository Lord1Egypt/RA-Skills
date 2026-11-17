## Description:

Cn Hex Decoder helps agents convert text to hexadecimal strings and decode hexadecimal strings with a small local Python helper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for quick local hex encoding and decoding during debugging, text inspection, and reverse-engineering workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documented capabilities, including color parsing, are not implemented by the provided Python helper.

Mitigation: Validate required behavior against the artifact before relying on those documented features; use the release primarily for encode and decode unless the helper is updated.

Risk: Invalid hex input decodes to null and usage errors are reported in Chinese, which can be ambiguous in automated workflows.

Mitigation: Check JSON results before using decoded values downstream and handle null or error responses explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-hex-decoder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local Python helper emits JSON; invalid hex decode input returns null.]

## Skill Version(s):

1.2.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
