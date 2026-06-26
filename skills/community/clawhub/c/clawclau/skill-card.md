## Description: <br>
ClawClau schedules Claude Code tasks in background tmux sessions and provides progress notifications, status checks, result retrieval, termination, and mid-task steering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BarryYJJ](https://clawhub.ai/user/BarryYJJ) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical operators use this skill to dispatch, monitor, steer, stop, and retrieve results from long-running Claude Code tasks without blocking the foreground agent session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended Claude Code sessions may run with permission safeguards disabled. <br>
Mitigation: Review before installing; run only in isolated workspaces and avoid high-impact repositories unless the launcher is patched or constrained. <br>
Risk: Task prompts, logs, or notifications may persist locally or be forwarded to Feishu/OpenClaw channels. <br>
Mitigation: Avoid secrets in prompts, consider --interval 0 and no Feishu chat for sensitive tasks, and regularly clean ~/.clawclau. <br>
Risk: Untrusted paths or model values can affect task launcher behavior. <br>
Mitigation: Use trusted workdirs and model names, and review script behavior before trusting it with untrusted inputs. <br>


## Reference(s): <br>
- [ClawClau schema and status reference](references/schema.md) <br>
- [ClawClau design principles and mechanisms](references/design.md) <br>
- [Clawclau on ClawHub](https://clawhub.ai/BarryYJJ/clawclau) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Files, Configuration instructions] <br>
**Output Format:** [Markdown with shell command examples plus text, stream-json, and local log outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write task registry, prompt backups, wrapper scripts, and logs under ~/.clawclau.] <br>

## Skill Version(s): <br>
2.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
