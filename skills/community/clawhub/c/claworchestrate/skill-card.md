## Description: <br>
Orchestrate AI agents across multiple machines by dispatching tasks, monitoring progress, and coordinating teams from a central gateway. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loop-capital](https://clawhub.ai/user/loop-capital) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a lightweight HTTP dispatcher on remote machines and send tasks to OpenClaw agents from a gateway host. It is intended for coordinated multi-machine agent work over private networking such as Tailscale or SSH-accessible environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose a network-accessible dispatch surface that starts OpenClaw agents on remote machines. <br>
Mitigation: Install only for intentional remote orchestration, bind the dispatcher to localhost or a private Tailscale interface, and avoid exposing port 9876 publicly. <br>
Risk: Weak credential configuration can allow unauthorized dispatch requests. <br>
Mitigation: Set a strong API key, avoid the changeme fallback, and prefer SSH tunneling or HTTPS/Tailscale-only transport. <br>
Risk: The included service installer can make the dispatcher persistent. <br>
Mitigation: Inspect or modify the systemd installer before enabling it as a persistent user service. <br>


## Reference(s): <br>
- [ClawOrchestrate on ClawHub](https://clawhub.ai/loop-capital/claworchestrate) <br>
- [Publisher profile: loop-capital](https://clawhub.ai/user/loop-capital) <br>
- [ClawStudio](https://clawstudio.co) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, HTTP API examples, and service configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and uses an API key for dispatcher authentication.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
