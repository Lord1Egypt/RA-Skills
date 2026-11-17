## Description:

Ganglion helps agents operate the Ganglion execution engine for Bittensor subnet mining, covering CLI commands, HTTP bridge APIs, pipeline execution, knowledge queries, configuration, and operational workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to scaffold and run Ganglion projects, inspect state, execute or mutate pipelines, query knowledge, and manage CLI, HTTP bridge, and MCP workflows for Bittensor subnet mining.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents unauthenticated local HTTP operations that can read project source, write executable code, alter pipelines and prompts, run jobs, and roll back changes.

Mitigation: Install only in a trusted development environment and keep the HTTP bridge bound to 127.0.0.1 unless authentication, TLS, firewalling, and access controls are added.

Risk: Runtime registration, prompt updates, pipeline patches, MCP connection, run, and rollback commands can change project behavior.

Mitigation: Require explicit review before using these commands, and prefer a virtual environment with pinned package versions.

## Reference(s):

- [Ganglion ClawHub Skill Page](https://clawhub.ai/tensorlink-dev/skills/ganglion)
- [Ganglion Project Homepage](https://github.com/TensorLink-AI/ganglion)
- [Commands & API Reference](references/commands.md)
- [Configuration Reference](references/configuration.md)
- [Operational Procedures](references/operations.md)
- [Troubleshooting](references/troubleshooting.md)
- [Common Workflows](examples/common-workflows.md)
- [Sample API Requests & Responses](examples/sample-requests.md)
- [Health Check Script](scripts/healthcheck.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, curl, JSON, and Python examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local CLI commands, HTTP API calls, MCP configuration guidance, and operational checks for Ganglion projects.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
