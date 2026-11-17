## Description:

Analyze log files to extract insights, errors, and patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect application, access, JSON, syslog, and web-server logs for errors, warnings, regex matches, and summary statistics during troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Log files may contain sensitive data that could be summarized, printed, or written to an output file.

Mitigation: Analyze only logs the user intends to inspect and choose output paths deliberately.

Risk: Complex regular expressions can make analysis slow or hang on large or crafted logs.

Mitigation: Use trusted, simple regex patterns and limit analysis scope for large files.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with inline shell commands; analyzer results are plain text or JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-specified local log files and can write user-directed JSON output files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
