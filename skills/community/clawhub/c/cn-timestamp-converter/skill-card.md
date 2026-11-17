## Description:

Converts Unix timestamps into UTC, local, and Chinese-readable date strings, automatically handling second- and millisecond-level inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[freedompixels](https://clawhub.ai/user/freedompixels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill during debugging and operations to convert Unix timestamps into readable UTC, local, and Chinese-formatted dates without external dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chinese-language labels and local date formatting may be misread in workflows expecting English labels or UTC-only output.

Mitigation: Confirm the expected locale and time zone before using converted timestamps in downstream decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/freedompixels/skills/cn-timestamp-converter)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON output and concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the Python standard library; accepts second- or millisecond-level Unix timestamps and defaults to the current time when no timestamp is provided.]

## Skill Version(s):

1.2.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
