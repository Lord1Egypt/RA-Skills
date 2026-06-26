## Description: <br>
Integrates OpenClaw with Claude Code CLI to delegate coding tasks via JSON queues for multi-turn code collaboration and analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gesilajerry](https://clawhub.ai/user/gesilajerry) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this skill to hand off coding, analysis, and multi-turn collaboration tasks to Claude Code through JSON queues and receive structured JSON results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queued tasks may receive broad automatic execution authority in the configured workspace. <br>
Mitigation: Review before installing, remove the permission-bypass flag unless the risk is accepted, and restrict queue and work directories. <br>
Risk: The artifact includes an embedded API token. <br>
Mitigation: Remove and rotate the embedded token, then configure credentials securely through environment or secret management. <br>
Risk: Prompts, outputs, and local logs may expose secrets or private code. <br>
Mitigation: Avoid submitting sensitive material unless local logs and result files are access-controlled and protected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gesilajerry/claude-code-collaboration) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [JSON result files containing task metadata, stdout, stderr, return code, and completion time.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses queue files for task input and result output; logs conversation and status files locally.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
