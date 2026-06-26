## Description: <br>
Runs bundled local PowerShell scripts from chat to report OpenClaw/Codex usage, manage idle alerts, set thresholds, and switch output language. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fantasyengineercdream](https://clawhub.ai/user/fantasyengineercdream) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users on Windows use this chat command to check Codex usage and manage idle usage alerts from Telegram or Feishu command channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read local OpenClaw auth and session files and use stored tokens to request usage data. <br>
Mitigation: Install only when the publisher and Windows chat-triggered usage-monitoring behavior are trusted, and review local token and session access before use. <br>
Risk: Auto alerts can create a hidden Windows scheduled task and send idle or usage details to a chat target inferred from recent activity. <br>
Mitigation: Enable auto alerts only when that background behavior and inferred target selection are acceptable; use the skill's auto status and auto off controls to inspect or disable it. <br>
Risk: Outbound usage checks may contact chatgpt.com with the stored token. <br>
Mitigation: Confirm that outbound access to chatgpt.com and use of the stored token are permitted in the deployment environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fantasyengineercdream/clawusage-windows-hardlock) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text command output from bundled PowerShell scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns stdout directly without model post-formatting; supports English and Chinese output modes.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
