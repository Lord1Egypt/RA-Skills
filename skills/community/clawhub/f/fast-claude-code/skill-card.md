## Description: <br>
Runs Claude Code tasks in background tmux sessions and sends completion callbacks for single, interactive, or team workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deadlining](https://clawhub.ai/user/deadlining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run Claude Code tasks asynchronously, coordinate multi-agent team work, and receive completion notifications without polling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run Claude Code unattended with broad project authority. <br>
Mitigation: Use --permission-mode plan unless the project is trusted and version-controlled. <br>
Risk: Team runs edit project Claude settings and install completion hooks. <br>
Mitigation: Inspect .claude/settings.json and .claude/hooks before and after team runs. <br>
Risk: Webhook or ntfy callbacks can transmit task content, source code, logs, or secrets. <br>
Mitigation: Avoid external callback destinations for sensitive prompts or outputs unless the destination is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/deadlining/fast-claude-code) <br>
- [DeadLining publisher profile](https://clawhub.ai/user/deadlining) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and shell command output with callback summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs through bash, Claude Code, tmux, and OpenClaw; jq is optional for general use and required for team hook management.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
