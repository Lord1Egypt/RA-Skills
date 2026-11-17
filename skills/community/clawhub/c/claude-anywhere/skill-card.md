## Description:

Claude Anywhere lets users operate Claude Code from Telegram, WeChat Work, or QQ to read and write files, execute commands, analyze images and files, manage code, resume sessions, and schedule tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yizhao1978](https://clawhub.ai/user/yizhao1978)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Claude Anywhere to access Claude Code from chat apps for remote code work, file analysis, command execution, session recovery, and scheduled automation across devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote chat users can control Claude Code against files and shell-accessible resources on the host.

Mitigation: Run the service under a dedicated unprivileged account and restrict bot access with explicit allowlists before deployment.

Risk: Disabled permission checks can amplify the impact of a mistaken or unauthorized prompt.

Mitigation: Remove --dangerously-skip-permissions and require operator review or tighter approval controls for sensitive actions.

Risk: Broad working-directory settings can expose more project or host data than intended.

Mitigation: Set CLAUDE_CWD and any knowledge directories to the narrowest required paths.

Risk: Persistent scheduled tasks can execute later without fresh human review.

Mitigation: Disable scheduled tasks or gate cron creation, listing, execution, and deletion to trusted operators.

Risk: Attachments and remote files can introduce untrusted content into analysis workflows.

Mitigation: Sanitize attachments and limit supported file handling to expected, low-risk content types.

Risk: Curl-to-sudo installation can run unaudited setup commands with elevated privileges.

Mitigation: Review installation commands and avoid elevated install paths unless they are strictly necessary.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yizhao1978/skills/claude-anywhere)
- [Claude Anywhere Homepage](https://claudeanywhere.com/buy.html)
- [QQ Bot OpenClaw Setup](https://q.qq.com/qqbot/openclaw/index.html)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Chat messages and Markdown with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file paths, command output summaries, code snippets, session references, and scheduled-task responses.]

## Skill Version(s):

1.6.2 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
