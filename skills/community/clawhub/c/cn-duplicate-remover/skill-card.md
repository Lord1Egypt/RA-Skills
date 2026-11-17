## Description:

Removes duplicate lines from text input or files, with options to preserve first-seen order or write the result to an output file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content maintainers, and agent operators can use this skill to remove repeated lines from supplied text or UTF-8 text files during cleanup and preparation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tool can overwrite a user-specified output file.

Mitigation: Review the output path before execution and write to a temporary file when preserving existing content matters.

Risk: Documentation and command help are in Chinese, which can lead to option misuse by readers who do not read Chinese.

Mitigation: Confirm the meaning of command options before running the script in an automated workflow.

Risk: Using the non-order-preserving mode can change line order.

Mitigation: Use the default order-preserving mode when downstream tasks depend on stable line order.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/freedompixels/skills/cn-duplicate-remover)
- [Publisher profile](https://clawhub.ai/user/freedompixels)
- [AISoBrand](https://aisobrand.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files]

**Output Format:** [Plain text output or UTF-8 text file, often accompanied by bash command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The CLI can read from inline text or a file and can write to a caller-provided output path.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
