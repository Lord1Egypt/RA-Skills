## Description:

CMDB Compass helps agents audit, remediate, and govern ServiceNow CMDBs with health scoring, duplicate detection, relationship analysis, stale CI cleanup, rollback, and audit trails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nexecuteinc](https://clawhub.ai/user/nexecuteinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, ServiceNow administrators, and CMDB owners use this skill to connect an MCP-compatible agent to ServiceNow for CMDB health analysis, duplicate and relationship checks, stale CI cleanup, and governed remediation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install script upgrades an unpinned PyPI package that will run with access to ServiceNow credentials.

Mitigation: Review the package and dependencies before installing, and prefer a pinned, hash-verified package version.

Risk: Write operations can merge, retire, bulk update, or repair CMDB records.

Mitigation: Use a dedicated least-privilege ServiceNow account and require dry runs, explicit human approval, change control, and tested rollback for write workflows.

## Reference(s):

- [CMDB Compass ClawHub Skill Page](https://clawhub.ai/nexecuteinc/skills/cmdbcompass)
- [CMDB Compass PyPI Package](https://pypi.org/project/cmdb-compass)
- [CMDB Compass Documentation Repository](https://github.com/cmdbcompass/cmdbcompass)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ServiceNow MCP configuration snippets and operational guidance for read-only audits or approved write workflows.]

## Skill Version(s):

1.0.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
