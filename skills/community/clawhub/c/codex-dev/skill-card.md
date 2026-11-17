## Description:

Run Codex as a background local job with an immediate receipt, saved logs and patch artifacts, optional Telegram notifications, and explicit workdir support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fzhlian](https://clawhub.ai/user/fzhlian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to dispatch Codex development tasks in the background, receive an immediate job receipt, and inspect saved logs, summaries, and patch artifacts later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package is incomplete if the claimed dispatcher, worker, or helper scripts are absent.

Mitigation: Verify the installed package contains the required executable scripts before relying on local wrappers or async job dispatch.

Risk: Copying the Telegram approval example as written can grant command-approval authority to a hardcoded Telegram account or an overly broad agent.

Mitigation: Replace approver IDs, restrict approvals to a dedicated trusted agent, and keep approval prompts in private chats unless the channel is trusted.

Risk: Telegram bot tokens and OpenClaw configuration values are sensitive local secrets.

Mitigation: Store tokens in local secret-aware configuration, avoid committing them, and rotate them if exposed.

Risk: The installer creates or overwrites command wrappers in the selected bin directory.

Mitigation: Install only into a bin directory where the wrapper names are expected and acceptable to replace.

## Reference(s):

- [Local setup](references/local-setup.md)
- [ClawHub skill page](https://clawhub.ai/fzhlian/skills/codex-dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local job receipts, logs, summaries, and patch artifacts under the configured jobs directory.]

## Skill Version(s):

0.1.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
