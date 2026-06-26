## Description: <br>
Ganglion helps agents operate the Ganglion execution engine for Bittensor subnet mining through its CLI, HTTP bridge API, pipeline execution, knowledge queries, configuration, and operational workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tensorlink-dev](https://clawhub.ai/user/tensorlink-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to scaffold, configure, run, inspect, mutate, and troubleshoot Ganglion projects for Bittensor subnet mining. It supports local CLI use, remote HTTP bridge operation, MCP integration, knowledge-store workflows, and rollback procedures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents broad control over a local or remote Ganglion bridge that can read project files, upload Python code, mutate pipelines, update prompts, run experiments, and roll back state. <br>
Mitigation: Install only when agent operation of Ganglion is intended, and review tool, agent, prompt, pipeline, and rollback changes before applying them. <br>
Risk: Exposing the HTTP bridge outside trusted boundaries can make source-read and mutation endpoints reachable by unintended users. <br>
Mitigation: Keep the bridge bound to localhost or a trusted admin network, and do not publicly expose source-read or mutation endpoints. <br>
Risk: API keys and shared knowledge may be exposed or reused incorrectly during operational workflows. <br>
Mitigation: Avoid printing API keys, verify environment handling, and inspect shared knowledge before using it in shared or production projects. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tensorlink-dev/ganglion) <br>
- [Publisher profile](https://clawhub.ai/user/tensorlink-dev) <br>
- [Project homepage](https://github.com/TensorLink-AI/ganglion) <br>
- [Commands and API Reference](artifact/references/commands.md) <br>
- [Configuration Reference](artifact/references/configuration.md) <br>
- [Operational Procedures](artifact/references/operations.md) <br>
- [Troubleshooting](artifact/references/troubleshooting.md) <br>
- [Common Workflows](artifact/examples/common-workflows.md) <br>
- [Sample API Requests and Responses](artifact/examples/sample-requests.md) <br>
- [Health Check Script](artifact/scripts/healthcheck.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration, Code, Markdown] <br>
**Output Format:** [Markdown with inline bash, JSON, curl, and Python configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, the ganglion CLI, and LLM_PROVIDER_API_KEY for normal operation.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
