## Description: <br>
Operate Emperor Claw as the OpenClaw control plane and durable checkpoint layer for an AI workforce. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josezuma](https://clawhub.ai/user/josezuma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to connect OpenClaw runtimes to Emperor Claw for runtime registration, task claiming, memory checkpointing, chat coordination, scoped resources, artifacts, and task result reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects an agent runtime to a third-party SaaS control plane that can sync state and perform task, chat, memory, artifact, and resource mutations. <br>
Mitigation: Install only when Emperor Claw is intended to be the remote system of record for the workspace, and review workspace access before deployment. <br>
Risk: The bridge relies on an API token and may post task notes, checkpoints, messages, and artifacts to the remote service. <br>
Mitigation: Use a least-privilege token when available, keep tokens out of committed files and chat, and avoid placing secrets or private user data in task, chat, memory, or artifact content. <br>
Risk: Automatic task claiming, checkpointing, and chat posting can affect production workflows if enabled without review. <br>
Mitigation: Run the bridge in a non-production workspace first and enable production only when automatic claiming, heartbeat renewal, and posting behavior are acceptable. <br>


## Reference(s): <br>
- [Control Plane Skill Page](https://clawhub.ai/josezuma/control-plane) <br>
- [Emperor Claw Setup](https://emperorclaw.malecu.eu/setup) <br>
- [API Reference](references/api.md) <br>
- [How Emperor Claw OS Works](references/HOW-IT-WORKS.md) <br>
- [Prerequisites](references/PREREQUISITES.md) <br>
- [Operational Lifecycle & Workflow](references/lifecycle.md) <br>
- [Roles & Memory Protocol](references/roles.md) <br>
- [Communication Guidelines](references/guidelines.md) <br>
- [Worked Examples](references/examples.md) <br>
- [Troubleshooting](references/TROUBLESHOOTING.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and JavaScript/Python bridge code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an Emperor Claw workspace token and writes state through Emperor Claw HTTP and WebSocket endpoints when used.] <br>

## Skill Version(s): <br>
1.14.15 (source: CHANGELOG and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
