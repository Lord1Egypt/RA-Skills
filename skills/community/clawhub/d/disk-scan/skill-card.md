## Description:

Scans a directory without changing files and ranks its largest files and subdirectories by size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system operators use this skill to find large files and folders when investigating local disk usage or planning cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release under-declares the read-only filesystem access and script execution needed to scan a directory; returned paths can reveal sensitive names.

Mitigation: Review before installing, declare required read access and execution, and scan only directories whose file and folder names are safe to expose.

Risk: Published usage examples include flags that the bundled script does not accept.

Mitigation: Use the script's supported --dir, --top, and --json flags; check --help before running.

## Reference(s):

- [disk-scan on ClawHub](https://clawhub.ai/zhaoxinghua09-cell/skills/disk-scan)
- [Publisher profile](https://clawhub.ai/user/zhaoxinghua09-cell)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Console text or optional JSON; agent can summarize findings in prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports total bytes and ranked file and subdirectory paths with sizes; does not delete files.]

## Skill Version(s):

1.0.5 (source: ClawHub release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
