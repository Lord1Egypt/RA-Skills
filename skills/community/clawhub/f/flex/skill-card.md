## Description:

Generate CSS Flexbox layouts using interactive CLI commands. Use when building responsive flex containers, rows, columns, or alignment configurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Flex to create, adjust, save, and export CSS Flexbox layout configurations from a command-line workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved layouts are written to ~/.flex/data.jsonl on the local system.

Mitigation: Review local storage expectations before use and avoid storing sensitive layout names or data in saved configurations.

Risk: Exports using --output can overwrite an existing file at the selected path.

Mitigation: Use stdout for review or choose a dedicated CSS export path before writing generated CSS.

## Reference(s):

- [Flex on ClawHub](https://clawhub.ai/bytesagain1/skills/flex)
- [BytesAgain homepage](https://bytesagain.com)
- [BytesAgain publisher profile](https://clawhub.ai/user/bytesagain1)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and CSS snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save layout records locally and export CSS to stdout or a user-selected file path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
