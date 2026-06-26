## Description: <br>
Diagnose and fix the 4 most common OpenClaw agent failures: heartbeat spam, API rate limit cascades, channel death loops, and memory/embedding errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agenthyjack](https://clawhub.ai/user/agenthyjack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose common OpenClaw agent health failures and apply practical remediation steps for logs, schedules, channels, memory files, and gateway configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested diagnostics and configuration changes can affect a live OpenClaw deployment if run directly on production systems. <br>
Mitigation: Review commands before execution, back up ~/.openclaw/openclaw.json before edits, and avoid unattended gateway restarts. <br>
Risk: External reference scripts are linked but not bundled with this skill. <br>
Mitigation: Inspect the external repository scripts separately before using them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agenthyjack/agent-health-diagnostics) <br>
- [agenthyjack publisher profile](https://clawhub.ai/user/agenthyjack) <br>
- [Collective Skills reference scripts](https://github.com/Bobalouie44/collective-skills/tree/main/references) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and configuration recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only troubleshooting output; no bundled scripts or generated files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
