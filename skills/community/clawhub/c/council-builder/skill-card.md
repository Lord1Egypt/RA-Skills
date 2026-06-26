## Description: <br>
Council Builder interviews a user, designs a 3-7 persona OpenClaw agent council, and generates the files, routing rules, learning metrics, and coordination docs needed to operate it. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Abdullah4AI](https://clawhub.ai/user/Abdullah4AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to turn workflow needs into a specialized local council of AI agent personas with per-agent files, coordination rules, adaptive routing, and self-improvement logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a persistent local agent-council workspace with memory and learning files that can retain sensitive details. <br>
Mitigation: Avoid storing secrets, credentials, personal data, regulated information, or confidential business details in generated memory, learning, config, and shared files; review those files periodically. <br>
Risk: Optional history scanning can read broad local context before the council is built. <br>
Mitigation: Ask the agent to skip history scanning unless explicit approval is given for the workspace and memory files to be inspected. <br>
Risk: Generated routing and coordination rules may be broader than intended for the user's actual workflow. <br>
Mitigation: Review and narrow the generated AGENTS.md, routing rules, coordination map, and per-agent permissions before relying on the council. <br>


## Reference(s): <br>
- [Council Builder ClawHub Page](https://clawhub.ai/Abdullah4AI/council-builder) <br>
- [Adaptive Routing](references/adaptive-routing.md) <br>
- [Coordination Patterns](references/coordination-patterns.md) <br>
- [Self Improvement](references/self-improvement.md) <br>
- [Soul Philosophy](references/soul-philosophy.md) <br>
- [Verification Patterns](references/verification-patterns.md) <br>
- [Example Councils](references/example-councils.md) <br>
- [Agent Scripts Patterns](references/agent-scripts-patterns.md) <br>
- [Config Patterns](references/config-patterns.md) <br>
- [Gotchas Patterns](references/gotchas-patterns.md) <br>
- [Hooks Patterns](references/hooks-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown files, JSON configuration, shell commands, and workspace directory structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates persistent local agent council files including AGENTS.md, SOUL.md, memory, learning logs, configuration, scripts, and shared reports.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
