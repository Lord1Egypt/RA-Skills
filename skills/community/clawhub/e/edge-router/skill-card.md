## Description:

Routes AI agent compute tasks to the cheapest viable backend across local inference (Ollama), cloud GPU (Vast.ai), and quantum hardware (Wukong 72Q).

This skill is ready for commercial/non-commercial use.

## Publisher:

[adjusternwachukwu-bot](https://clawhub.ai/user/adjusternwachukwu-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Edge Router to choose among local, cloud GPU, and quantum compute backends, check availability, and execute workloads with cost-aware routing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public API routing can send prompts, payloads, datasets, or workloads to external compute providers.

Mitigation: Avoid sending secrets, private prompts, proprietary datasets, or regulated data unless the service and external routing path are approved; use localhost for local-only testing.

## Reference(s):

- [Edge Router API](https://edge-router.gpupulse.dev/api/v1)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Describes API calls for routing, execution, backend status, statistics, and health checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
