## Description:

Convert JSON arrays of objects into CSV format using local Expanso Edge CLI or MCP workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aronchick](https://clawhub.ai/user/aronchick)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to convert JSON object arrays into CSV strings for data export, spreadsheet generation, report creation, and API response formatting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: MCP server mode binds broadly by default and could be reachable from untrusted networks.

Mitigation: Bind the server to 127.0.0.1 or place it behind a firewall before use.

Risk: CSV generated from untrusted JSON can be unsafe to open directly in spreadsheet tools.

Mitigation: Treat generated CSV as untrusted unless formula neutralization and complete CSV escaping are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aronchick/skills/expanso-json-to-csv)
- [Expanso website](https://expanso.io)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON output descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill returns a CSV string with row count, detected columns, and metadata.]

## Skill Version(s):

1.0.0 (source: server release and skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
