## Description: <br>
Build and manage Apple-native container dev environments with ciderbox and orchard swarm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mentholmike](https://clawhub.ai/user/mentholmike) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill on Apple Silicon Macs to create local container VMs, test projects across Linux distro images, scaffold ciderbox and orchard configuration, and run local OpenClaw agent swarms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides agents to create local container VMs, run commands, sync workspaces, and launch local OpenClaw agent swarms. <br>
Mitigation: Use it only for projects where local container execution and agent-swarm access are intended, and review generated commands before running them. <br>
Risk: Orchard workflows can push .orchid.env secrets into running VMs. <br>
Mitigation: Validate required secrets before pushing them, limit use to trusted local VMs, and run the documented teardown commands when finished. <br>


## Reference(s): <br>
- [Ciderbox ClawHub listing](https://clawhub.ai/mentholmike/ciderbox) <br>
- [Publisher profile](https://clawhub.ai/user/mentholmike) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell and YAML code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for local Apple container workflows and may include commands that create VMs, sync workspaces, launch agents, or push .orchid.env secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
