## Description:

Format Tool provides local command-line text transformations for case changes, wrapping, trimming, sorting, deduplication, reversing, and whitespace removal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to clean up local text input from arguments or stdin, including case conversion, line sorting, deduplication, wrapping, trimming, reversing, and whitespace removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation advertises JSON, CSV, table, column alignment, padding, and separator features that are not implemented in the inspected script.

Mitigation: Use the implemented text commands only, and verify behavior before relying on advertised structured-data formatting.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/format-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text and concise Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates on local stdin or an optional text argument; wrapping accepts a width parameter.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
