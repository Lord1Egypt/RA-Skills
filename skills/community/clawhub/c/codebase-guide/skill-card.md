## Description:

Guides agents through Ganglion project operations, including CLI commands, HTTP bridge API usage, pipeline execution, knowledge queries, configuration, troubleshooting, and operational workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to run and inspect Ganglion projects, scaffold configurations, operate local or HTTP bridge modes, manage pipelines, query knowledge, troubleshoot failures, and perform controlled runtime changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-activates broadly and can guide agents through powerful Ganglion operations such as live mutation, rollback, MCP expansion, and project-source access.

Mitigation: Install only for trusted Ganglion projects and require explicit approval before pipeline, prompt, policy, rollback, or MCP changes.

Risk: HTTP bridge workflows can expose operational control if bound to an untrusted network.

Mitigation: Keep the HTTP bridge bound to localhost or another trusted network.

Risk: Tool and agent registration endpoints accept code-like definitions that can change runtime behavior.

Mitigation: Review submitted code before using tool or agent registration endpoints.

Risk: Troubleshooting commands and project inspection can execute Python against local project files.

Mitigation: Avoid running troubleshooting Python execution commands on untrusted projects and prefer a virtual environment with pinned reviewed package versions.

Risk: OPENAI_API_KEY is required for pipeline execution and may be exposed through careless terminal or log handling.

Mitigation: Do not expose OPENAI_API_KEY in shared logs or terminals.

## Reference(s):

- [Codebase Guide on ClawHub](https://clawhub.ai/tensorlink-dev/skills/codebase-guide)
- [Ganglion Project Homepage](https://github.com/TensorLink-AI/ganglion)
- [Commands & API Reference](references/commands.md)
- [Configuration Reference](references/configuration.md)
- [Operational Procedures](references/operations.md)
- [Troubleshooting](references/troubleshooting.md)
- [Common Workflows](examples/common-workflows.md)
- [Sample API Requests & Responses](examples/sample-requests.md)
- [Healthcheck Script](scripts/healthcheck.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with bash, curl, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, ganglion, and OPENAI_API_KEY according to server-resolved metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
