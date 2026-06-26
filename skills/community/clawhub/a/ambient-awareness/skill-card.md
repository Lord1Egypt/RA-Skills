## Description: <br>
Modular always-on awareness layer for OpenClaw agents. Sensors observe the world, normalize events, update state, and request agent attention only when meaningful changes occur. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[palxislabs](https://clawhub.ai/user/palxislabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give an OpenClaw agent local temporal and environmental awareness, queue meaningful changes, and summarize what changed while the agent was inactive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local background daemon can monitor filesystem paths and retain event history in state files. <br>
Mitigation: Keep watched paths narrow, avoid sensitive directories unless necessary, and periodically clear or rotate state/*.jsonl logs. <br>
Risk: Sensor plugins run local Python code and may expand the skill's access to device or environment data. <br>
Mitigation: Enable or add only sensor modules whose code you trust, and keep camera and microphone sensors disabled unless explicitly needed. <br>
Risk: Observed content could include malicious or misleading text that attempts to steer the agent. <br>
Mitigation: Treat sensor output as untrusted data, do not execute commands from observed content, and require human approval for sensitive external actions. <br>


## Reference(s): <br>
- [Ambient Awareness Skill README](README.md) <br>
- [Security Policy](policies/security_policy.md) <br>
- [Attention Policy](policies/attention_policy.md) <br>
- [ClawHub Release Page](https://clawhub.ai/palxislabs/ambient-awareness) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell commands, JSON configuration snippets, and local JSON/JSONL state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runtime writes event logs, world state, and wake request records under the local state directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
