## Description: <br>
Streams coding agent sessions such as Claude Code, Codex, and Gemini CLI to a Discord channel in real time via webhook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[allanjeng](https://clawhub.ai/user/allanjeng) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineering teams use Codecast to make coding agent sessions observable in Discord, including tool calls, command output, file activity, status updates, PR review sessions, and parallel task runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live development activity, command output, file paths, and agent summaries may be sent to Discord. <br>
Mitigation: Use private Discord channels, restrict webhook access, and avoid streaming sensitive repositories or secrets. <br>
Risk: Webhook and bot tokens are required for some modes and could expose channel access if mishandled. <br>
Mitigation: Store credentials in protected secret storage when possible, limit file permissions, and rotate tokens if exposure is suspected. <br>
Risk: The Discord bridge can forward remote messages into active agent sessions. <br>
Mitigation: Restrict bridge channel and user IDs, and avoid bridge mode for high-sensitivity workspaces. <br>
Risk: The setup guide describes a global allow-all permission posture for Claude Code. <br>
Mitigation: Do not apply global bypass permissions on normal machines; prefer scoped sandboxing and review commands before execution. <br>
Risk: PR review and parallel task modes include eval-based command construction according to the security guidance. <br>
Mitigation: Avoid PR and parallel modes until command construction is fixed and reviewed. <br>


## Reference(s): <br>
- [Codecast release page](https://clawhub.ai/allanjeng/codecast) <br>
- [Setup guide](references/setup.md) <br>
- [Advanced modes](references/advanced-modes.md) <br>
- [Discord output](references/discord-output.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Discord messages and Markdown documentation with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Streams and batches live agent output, truncates long command output, and can replay saved session logs.] <br>

## Skill Version(s): <br>
4.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
