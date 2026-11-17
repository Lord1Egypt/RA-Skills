## Description:

System health monitoring and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eternal0404](https://clawhub.ai/user/eternal0404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check local CPU, memory, disk, process, and network health and generate system-health reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports can expose host details, IP addresses, mount information, and process command snippets.

Mitigation: Limit report sharing and storage, and redact sensitive host or process details before external use.

Risk: Network health checks perform an external DNS lookup to google.com.

Mitigation: Run network checks only where that lookup is acceptable, or use category-specific checks that do not require network probing.

Risk: Running with elevated privileges can reveal more local system and process information than necessary.

Mitigation: Run with least privilege unless elevated access is specifically required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eternal0404/skills/eternal-system-health)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown with bash command examples and plain-text system health reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include host details, IP addresses, mount information, and process command snippets; optional output writes reports to a file.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
