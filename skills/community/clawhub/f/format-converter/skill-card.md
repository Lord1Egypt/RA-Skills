## Description:

Converts data between CSV, JSON, XML, YAML, and TOML, with support for batch conversion, nested structure handling, encoding guidance, formatting, and error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data analysts, and automation users use this skill to convert structured data files between common formats for analysis, reporting, and workflow integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read local source data files and write converted outputs.

Mitigation: Use trusted input files, confirm output paths, and choose a fresh output directory or verify overwrite behavior before batch conversions.

Risk: Callback URLs can disclose converted data or status information to an external endpoint.

Mitigation: Use callback_url only with trusted endpoints and only when the user understands what information will be sent.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/format-converter)
- [Skill source file](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code snippets and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce converted file content, conversion steps, error handling guidance, or batch-processing instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
