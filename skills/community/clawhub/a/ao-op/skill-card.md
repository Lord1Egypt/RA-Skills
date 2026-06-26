## Description: <br>
Ao Op helps an agent invoke a local Agent Orchestrator source checkout through a stable wrapper for health checks, service control, sessions, messaging, review checks, and updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chaoyang78](https://clawhub.ai/user/chaoyang78) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to operate a local AO checkout from an agent session when managing orchestrator services, sessions, messages, review feedback, or source updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AO wrapper commands can change running sessions, local source files, dependencies, or generated build output. <br>
Mitigation: Run only the intended AO command, confirm the target project or session first, and treat start, stop, send, update, git pull, pnpm install, and pnpm build as deliberate state-changing actions. <br>
Risk: The wrapper depends on a documented local AO checkout path. <br>
Mitigation: Install only where that checkout is expected, and verify the path before relying on the wrapper. <br>


## Reference(s): <br>
- [AO command cookbook](references/commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for a local AO source checkout and may affect local sessions, files, dependencies, or build output.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
