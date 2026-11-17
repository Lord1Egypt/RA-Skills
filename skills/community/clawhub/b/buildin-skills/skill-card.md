## Description:

Use the Buildin CLI safely for authorized API, content, and file tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[buildin](https://clawhub.ai/user/buildin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect Buildin CLI help and authentication state, then run authorized Buildin API, page, database, search, Markdown, and file workflows with explicit approval for sensitive actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer, update, login, upload, create, and update actions can affect the local environment or remote Buildin workspace.

Mitigation: Confirm trust in Buildin and approve only the exact workspace, target, content, and action intended before proceeding.

Risk: Bearer tokens or credentials could be exposed if pasted into chat, command arguments, logs, files, or request bodies.

Mitigation: Use environment variables, saved credentials, or an approved secret channel, and redact any credential that appears in command output.

Risk: Expired or invalid credentials, including HTTP 401 responses, can lead to incomplete or misleading API work.

Mitigation: Verify authentication with Buildin doctor and identity checks before remote API calls, and refresh credentials before retrying failed API work.

## Reference(s):

- [Buildin CLI skill release](https://clawhub.ai/buildin/skills/buildin-skills)
- [Buildin CLI installer](https://cdn.buildin.ai/buildin-cli/install)
- [Buildin CLI Windows installer](https://cdn.buildin.ai/buildin-cli/install.ps1)
- [Buildin API base URL](https://api.buildin.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use Buildin CLI JSON output for authenticated API operations.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
