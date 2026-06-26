## Description: <br>
Memory graph engine with caller-provided embed and LLM callbacks; core is pure, with real-time correction flow and optional OpenAI integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jonathangu](https://clawhub.ai/user/jonathangu) <br>

### License/Terms of Use: <br>
Apache-2.0 <br>


## Use Case: <br>
Developers and agent builders use CrabPath to build and maintain a learned memory graph over selected workspaces so agents can retrieve, suppress, inject, and update context through CLI and Python APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently change agent memory and workspace-derived state. <br>
Mitigation: Require explicit approval for learn, inject, sync, maintain, merge, prune, and compact actions in high-trust environments. <br>
Risk: Workspace, query, journal, or fired-log data may contain sensitive information. <br>
Mitigation: Restrict indexed workspace and session paths, prefer hash or local operation for sensitive data, and secure or rotate generated logs. <br>
Risk: Optional OpenAI-backed adapters can send selected content to an external provider. <br>
Mitigation: Review each OpenAI-backed example or adapter before use and enable provider-backed callbacks only where approved. <br>


## Reference(s): <br>
- [CrabPath site](https://jonathangu.com/crabpath/) <br>
- [Architecture documentation](docs/architecture.md) <br>
- [Setup guide](docs/setup-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/jonathangu/crabpath) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; runtime CLI and API output can be text or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains persistent state in state.json and optional journals or fired logs when configured.] <br>

## Skill Version(s): <br>
11.2.1 (source: server release metadata and pyproject.toml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
