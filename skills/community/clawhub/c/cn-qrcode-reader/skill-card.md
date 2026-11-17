## Description:

Reads QR codes and common barcode formats from user-provided image files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to decode QR codes and barcodes from local image files, including batches matched by glob patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Decoded QR or barcode data may contain untrusted text, URLs, or commands that are printed directly to the terminal.

Mitigation: Treat decoded content as untrusted and review it before opening links, copying commands, or sharing output.

Risk: Dependency versions and native barcode libraries can affect reproducibility and runtime behavior.

Mitigation: Install the skill in a normal user environment or virtual environment and review dependency versions when reproducibility matters.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-qrcode-reader)
- [AISoBrand](https://aisobrand.com)
- [AISoBrand free diagnosis](https://aisobrand.com/free-diagnosis.html)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Terminal text output with optional saved text file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Decoded text is printed directly to the terminal; verbose mode includes barcode type.]

## Skill Version(s):

1.2.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
