## Description: <br>
Check Claude Code / Claude Max usage limits when a user asks about usage, limits, quota, or remaining Claude capacity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aligurelli](https://clawhub.ai/user/aligurelli) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to check local Claude CLI usage limits, quota, reset times, and spending-limit information for the account currently logged in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill briefly controls the local Claude CLI and reads Claude usage, quota, reset-time, and spending-limit information. <br>
Mitigation: Run it only when the user intends to check that information, and confirm the Claude CLI is logged into the intended account before use. <br>
Risk: The skill requires an interactive PTY and a locally installed, authenticated Claude CLI. <br>
Mitigation: If the CLI is missing or reports a missing API key, stop and ask the user to install Claude Code or complete the local browser login flow before retrying. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aligurelli/claude-usage-checker) <br>
- [Publisher profile](https://clawhub.ai/user/aligurelli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown table with concise explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports usage percentages, reset times, and extra usage spending-limit status from the local Claude CLI.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
