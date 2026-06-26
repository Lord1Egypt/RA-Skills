## Description: <br>
Evoclaw (Evolved) helps an agent install and operate a self-evolving identity framework that logs experiences, reflects on them, and updates SOUL.md through governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[shuoyu017](https://clawhub.ai/user/shuoyu017) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to configure an OpenClaw agent that maintains durable memory, classifies experiences, reflects on them, proposes identity changes, and runs validators under configurable governance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for durable memory and ongoing authority to evolve an agent's SOUL.md over time. <br>
Mitigation: Use supervised governance before enabling it, review proposed SOUL.md changes, and periodically inspect or delete memory and telemetry files. <br>
Risk: External social sources and credential setup can expand data exposure if enabled casually. <br>
Mitigation: Keep external sources disabled unless needed, use environment variables for credentials, and do not paste raw API keys for automatic shell-profile storage. <br>
Risk: Heartbeat and local-file workflows can modify agent operating files outside the immediate conversation. <br>
Mitigation: Review all AGENTS.md and HEARTBEAT.md changes and run the included validators before relying on the updated workspace. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/shuoyu017/evoclaw-evolved) <br>
- [EvoClaw Configuration](artifact/README.md) <br>
- [EvoClaw Configuration Guide](artifact/configure.md) <br>
- [EvoClaw Data Schemas Reference](artifact/references/schema.md) <br>
- [EvoClaw Pipeline Examples](artifact/references/examples.md) <br>
- [Heartbeat Debugging Guide](artifact/references/heartbeat-debug.md) <br>
- [EvoClaw Source API Reference](artifact/references/sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown operating manual with JSON schemas, Python helper scripts, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead an agent to create or update memory, SOUL.md, AGENTS.md, HEARTBEAT.md, telemetry, and configuration files in its workspace.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
