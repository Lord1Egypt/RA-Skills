## Description:

Helps OpenClaw orchestrators identify recurring workloads, create specialized sub-agents, evaluate them, route tasks, and monitor their lifecycle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samajesteduroyaume](https://clawhub.ai/user/samajesteduroyaume)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to identify repeat tasks, create and evaluate specialized sub-agents, and route and monitor their work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Powerful local factory actions have weak access controls and safety gates.

Mitigation: Install only in a tightly isolated workspace; review authorization, path containment, archive validation, and benchmarking before enabling production actions.

Risk: The dashboard may expose factory operations if reachable over a network.

Mitigation: Do not expose the dashboard to a network until authentication and localhost binding are fixed.

Risk: Task content may be saved locally or sent to configured LLM or webhook endpoints.

Mitigation: Avoid sensitive task data until data handling, endpoint configuration, and secret-key handling are reviewed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/samajesteduroyaume/skills/agent-factory-2)
- [Source repository (server-resolved provenance)](https://github.com/samajesteduroyaume/Agent-Factory)
- [Sub-agent manifest schema](artifact/skills/agent-factory/references/manifest_schema.json)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance, command examples, and JSON sub-agent manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local telemetry, evaluation results, and agent configuration files.]

## Skill Version(s):

0.1.0 (source: ClawHub release; bundled skill frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
