## Description:

Guides three read-only codebase audits covering security and privacy, database integrity and performance, and architecture and resilience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bergschloss](https://clawhub.ai/user/bergschloss)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security reviewers use this skill to inspect a defined codebase scope and document potential vulnerabilities, database issues, and architectural weaknesses without changing project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill suggests switching to PowerShell to write reports when direct file-write permission is unavailable.

Mitigation: Review and remove that instruction before installation; stop or request an approved output directory if report writes are denied.

Risk: Persistent Desktop reports and optional subagent files may contain sensitive code or findings.

Mitigation: Approve the report destination, limit access to generated files, and review reports before sharing or retaining them.

## Reference(s):

- [Source repository](https://github.com/Bergschloss/forensic-audit)
- [ClawHub skill listing](https://clawhub.ai/bergschloss/skills/forensic-audit)
- [File-by-file audit pipeline example](artifact/tasks-forensic-example.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Timestamped Markdown audit reports and a brief chat summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three sequential phase reports with severity counts and file:line findings; optional consolidated pipeline report.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
