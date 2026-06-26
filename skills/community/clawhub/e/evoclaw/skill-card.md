## Description: <br>
Manages a self-evolving AI identity by logging experiences, reflecting on them, proposing updates, and governing changes to a structured SOUL.md file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eyedark](https://clawhub.ai/user/eyedark) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use Evoclaw to install and run an agent identity-evolution workflow with durable memory, reflection artifacts, proposal review, governance modes, and SOUL.md change logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to keep durable conversation memory and evolve an agent identity over time. <br>
Mitigation: Install it only when that behavior is intended, and review SOUL.md, memory files, AGENTS.md, and HEARTBEAT.md before first use. <br>
Risk: Default autonomous governance can apply MUTABLE identity changes automatically. <br>
Mitigation: Start with supervised governance or review pending proposals and change logs until the workflow is trusted. <br>
Risk: Setup and external feed configuration may involve API credentials. <br>
Mitigation: Use environment variables, avoid pasting raw API tokens into prompts when possible, and review shell profile changes. <br>
Risk: The optional visualizer server can expose workspace state and write behavior if reachable from untrusted networks. <br>
Mitigation: Run the visualizer only on a trusted local interface unless its write endpoint is protected or disabled. <br>


## Reference(s): <br>
- [Evoclaw on ClawHub](https://clawhub.ai/eyedark/evoclaw) <br>
- [Configuration Guide](README.md) <br>
- [Data Schemas Reference](references/schema.md) <br>
- [Worked Pipeline Examples](references/examples.md) <br>
- [Source API Reference](references/sources.md) <br>
- [Heartbeat Debugging Guide](references/heartbeat-debug.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with JSON and JSONL schemas, Python validators, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and validates SOUL.md structure, memory logs, reflection artifacts, proposals, state files, change logs, and optional visualization assets in the agent workspace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
