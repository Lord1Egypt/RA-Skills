## Description:

Disk Space Analyzer scans local disk drives, identifies top space consumers and cache locations, and helps an agent generate a disk usage report with optimization guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raingingkleec](https://clawhub.ai/user/raingingkleec)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, support staff, and end users use this skill to inspect local disk usage, produce an HTML report, identify large directories and caches, and prioritize cleanup or migration actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can expose hostnames, full paths, directory names, cache locations, and Windows component sizes.

Mitigation: Keep reports local, review them before sharing, and redact sensitive paths or machine identifiers when distribution is necessary.

Risk: The HTML report generation can render untrusted file or folder names unsafely.

Mitigation: Escape report data or render it through safe DOM/text APIs before opening reports from systems with untrusted filenames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/raingingkleec/skills/disk-space-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [JSON scan data, HTML report, and concise Markdown/text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may contain hostnames, full paths, directory names, cache locations, and Windows component sizes.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
