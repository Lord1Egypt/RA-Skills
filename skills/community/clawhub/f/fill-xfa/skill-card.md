## Description:

This skill helps agents inspect and fill Adobe LiveCycle XFA PDF forms by discovering XML-backed fields and writing values into a filled PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kiagentkronos-cell](https://clawhub.ai/user/kiagentkronos-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, and external users can use this skill to automate field discovery and data entry for XFA PDFs that standard AcroForm tools cannot fill. It is suited to government, utility, school, and similar forms that require a filled PDF output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Filled form values can include personal or sensitive information and may be printed to terminal output by default.

Mitigation: Run the script only where terminal output is not captured, patch or suppress value printing before handling real forms, and avoid storing logs that contain filled values.

Risk: Incorrect field names or duplicate fields can lead to incomplete or incorrect filled PDFs.

Mitigation: Use the field discovery command first, keep an untouched source PDF, and validate the filled PDF before submission.

Risk: The Python dependency and PDF-processing workflow can add supply-chain and file-handling risk.

Mitigation: Install pikepdf in an isolated environment with pinned versions where possible and use an explicit output file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kiagentkronos-cell/skills/fill-xfa)
- [Publisher profile](https://clawhub.ai/user/kiagentkronos-cell)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and generated PDF files when the script is run]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires pikepdf and an input PDF with XFA form data; field values may be supplied through JSON, stdin, or repeated key-value arguments.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
