## Description: <br>
Helps AI agents act more proactively, preserve context through local memory files, and improve continuously using WAL, working buffer, and recovery patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[engsathiago](https://clawhub.ai/user/engsathiago) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure agents for proactive check-ins, local persistent memory across context loss, and continuous self-improvement. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proactive monitoring and local persistent memory can capture exchanges or context beyond what the user intended. <br>
Mitigation: Set explicit rules for what the agent may monitor, when it may act without being asked, what may be written into .autonomia, how long those files are kept, and how to review or delete them. <br>
Risk: Continuous self-improvement and recovery routines can change agent behavior over time. <br>
Mitigation: Review generated memory, learning, and recovery files before relying on them, and keep clear guardrails for autonomous actions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/engsathiago/autonomia-agente) <br>
- [Project homepage](https://github.com/eve-agent/autonomia-agente) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file layout guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct agents to create or maintain local .autonomia memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
