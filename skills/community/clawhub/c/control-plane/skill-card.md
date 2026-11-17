## Description:

Operate Emperor Claw as the OpenClaw control plane and durable checkpoint layer for an AI workforce.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josezuma](https://clawhub.ai/user/josezuma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect OpenClaw runtimes to Emperor Claw for task claims, durable memory checkpoints, chat/status coordination, artifacts, incidents, and scoped resource handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The hosted control plane can direct and record broad AI workforce activity.

Mitigation: Install only when Emperor Claw is intended to be the system of record for the workforce, and scope deployment to runtimes that should follow that control plane.

Risk: Workspace tokens, task content, chat, memory, and logs can expose sensitive operational data.

Mitigation: Use least-privilege tokens, keep tokens out of checked-in configuration, and avoid placing secrets or private prompts in remote tasks, chat, or memory.

Risk: Remote messages and memory may contain under-scoped or unsafe instructions.

Mitigation: Treat remote control-plane content as untrusted input that cannot override local safety rules, approval gates, or operator policy.

Risk: A misdirected API or WebSocket origin could route workforce state to the wrong service.

Mitigation: Pin the API and WebSocket origins to the documented official HTTPS/WSS host before connecting bridge adapters.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/josezuma/skills/control-plane)
- [Publisher Profile](https://clawhub.ai/user/josezuma)
- [Emperor Claw MCP API Reference](artifact/references/api.md)
- [How Emperor Claw OS Works](artifact/references/HOW-IT-WORKS.md)
- [Operational Lifecycle & Workflow](artifact/references/lifecycle.md)
- [Emperor Claw Roles & Ownership](artifact/references/roles.md)
- [Agent Communication Guidelines](artifact/references/guidelines.md)
- [Worked Examples](artifact/references/examples.md)
- [Prerequisites](artifact/references/PREREQUISITES.md)
- [Troubleshooting](artifact/references/TROUBLESHOOTING.md)
- [Emperor Claw Setup](https://emperorclaw.malecu.eu/setup)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with inline API payloads, shell commands, and reference bridge code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are operational guidance for connecting a local OpenClaw runtime to the hosted control plane; execution still happens in the local runtime.]

## Skill Version(s):

1.14.15 (source: package.json, CHANGELOG, server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
