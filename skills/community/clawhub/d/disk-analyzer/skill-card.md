## Description:

Disk Analyzer helps an agent inspect disk usage and free space, find large or duplicate files, monitor usage, and export disk reports with a shell utility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bytesagain1](https://clawhub.ai/user/bytesagain1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and support engineers use this skill to inspect local disk usage, identify large or duplicate files, monitor usage changes, and export disk reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted or unusual path arguments can make file-search commands behave unexpectedly, especially path values beginning with a dash.

Mitigation: Review command arguments before execution and use trusted, explicit paths that do not begin with a dash.

Risk: The cleanup command reports broad system cleanup locations rather than behaving as a path-scoped analyzer.

Mitigation: Treat cleanup output as advisory, review each suggested location manually, and do not perform cleanup actions solely from this report.

## Reference(s):

- [muesli/duf](https://github.com/muesli/duf)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Plain text, Markdown, or JSON disk usage reports with shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated from local filesystem commands and may vary by operating system, permissions, mounted filesystems, and command arguments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
