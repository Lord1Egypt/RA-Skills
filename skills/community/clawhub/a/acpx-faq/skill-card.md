## Description:

Run coding agents (codex, claude, agy) through the acpx ACP CLI for one-shot dispatch into named sessions you can watch live.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tenequm](https://clawhub.ai/user/tenequm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this guide to launch and monitor coding agents through acpx and troubleshoot command failures, missing sessions, and lost prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The guide advises bypassing approval rules and prompt screening.

Mitigation: Remove those override and bypass instructions before use.

Risk: Its setup command can overwrite existing settings.

Mitigation: Review the command and preserve existing settings when configuring authentication.

Risk: Unattended agent runs may use inherited credentials or reach unintended provider accounts and projects.

Mitigation: Authorize a specific task, use an enforced sandbox, and verify the provider, account, project access, and inherited credentials.

Risk: Failed sessions and retained logs may persist after a run.

Mitigation: Close failed sessions and consider retained logs.

## Reference(s):

- [acpx project](https://github.com/openclaw/acpx)
- [Antigravity ACP registry entry](https://github.com/agentclientprotocol/registry/blob/main/antigravity-acp/agent.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with shell command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.11.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
