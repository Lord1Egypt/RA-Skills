## Description:

Helps agents install, run, and troubleshoot Flydb CLI release packages, including migration dry runs and execution, local web workbench use, JSON and Plan output, MCP calls, and JDBC driver setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzxcoding](https://clawhub.ai/user/zzxcoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, database operators, and release engineers use this skill to manage Flydb CLI setup, database migration checks, controlled execution, local web workflows, MCP tool usage, and JDBC driver troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to run downloaded Flydb CLI release packages.

Mitigation: Prefer an already-installed or locally supplied Flydb CLI and verify the ZIP hash or signature independently before use.

Risk: Database migration commands can write to or destructively alter target databases.

Mitigation: Use validate and dry-run or plan review before production writes, require explicit scoped approval, and run with least-privileged database accounts.

Risk: JDBC drivers may be dynamically loaded or downloaded.

Mitigation: Prefer approved local or internal-repository driver artifacts, use driver-download=never or offline for agent-run operations, and respect vendor driver licenses.

Risk: Database credentials can leak through command lines, config files, logs, or reports.

Mitigation: Use environment variables or password files, redact JDBC URLs, and avoid storing real passwords in shared config files or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zzxcoding/skills/flydb-cli-release)
- [Publisher profile](https://clawhub.ai/user/zzxcoding)
- [Release package reference](references/release-package.md)
- [CLI commands reference](references/commands.md)
- [Configuration reference](references/configuration.md)
- [Errors reference](references/errors.md)
- [JDBC drivers reference](references/drivers.md)
- [JDBC integration reference](references/jdbc-integration.md)
- [JSON output reference](references/json-output.md)
- [Plan Artifact reference](references/plan-artifact.md)
- [MCP tools reference](references/mcp-tools.md)
- [Local web workbench reference](references/web.md)
- [Local web API reference](references/web-api.md)
- [Upstream sync record](references/upstream-sync.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run plans, status summaries, version checks, and credential redaction guidance.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
