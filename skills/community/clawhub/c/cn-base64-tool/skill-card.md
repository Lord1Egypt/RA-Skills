## Description:

Cn Base64 Tool provides a local Python standard-library utility for Base64 encoding and decoding strings and files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to encode text or file contents as Base64 and decode Base64 content back into text or files using a small local Python script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File decode operations can overwrite content at a user-specified output path.

Mitigation: Use explicit non-critical output paths and review the target path before running decode_file.

Risk: Chinese-language documentation includes stale or unsupported examples, including commands not implemented by the bundled script.

Mitigation: Confirm supported commands against the bundled Python script and use the implemented encode, decode, encode_file, and decode_file subcommands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-base64-tool)
- [Publisher profile](https://clawhub.ai/user/freedompixels)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands, Guidance]

**Output Format:** [Plain text, local files, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with the Python standard library; file decode operations write to user-specified output paths.]

## Skill Version(s):

1.2.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
