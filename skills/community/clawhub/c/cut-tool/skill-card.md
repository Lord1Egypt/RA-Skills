## Description:

Extract specific fields or columns from text files using delimiter-based parsing. Use when you need to select columns from CSV, TSV, or delimited data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data-processing users use this skill to request extraction of fields or character ranges from delimited text such as CSV, TSV, and logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently truncate data instead of extracting the requested fields.

Mitigation: Review the shipped script behavior against expected cut-style field extraction before installing or using it in data-processing workflows.

Risk: Users may rely on misleading output from delimited-file processing.

Mitigation: Run representative test inputs and compare output against the requested field or character selection before using results downstream.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dinghaibin/skills/cut-tool)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples; script output is plain text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Security evidence reports that the shipped script may silently truncate each input line rather than extracting requested fields.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
