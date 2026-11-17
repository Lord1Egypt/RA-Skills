## Description:

Encode and decode base64 data with support for standard and URL-safe variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to encode text or files to Base64 and decode Base64 input, including URL-safe variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can read any input file path explicitly passed by the user and write transformed output to an explicitly chosen path.

Mitigation: Run it only on files intended for Base64 transformation and choose output paths deliberately to avoid exposing or overwriting sensitive data.

Risk: Decoded Base64 may produce binary data or text that is not valid UTF-8.

Mitigation: Write decoded binary output to a file and inspect it with an appropriate tool instead of relying on terminal display.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/dinghaibin-base64-tool)

## Skill Output:

**Output Type(s):** [Text, Files, Shell commands]

**Output Format:** [Plain text Base64 strings, decoded text, or decoded binary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports standard and URL-safe Base64 and optional line wrapping for encoded strings.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
