## Description:

Agent Guardian helps OpenClaw-based assistants monitor work state, report status, answer status queries, filter mixed-language replies, and track message processing queues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanxinyun1991](https://clawhub.ai/user/fanxinyun1991)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to add watchdog checks, status reporting, immediate status responses, language-consistency filtering, and queue visibility to OpenClaw channel integrations such as QQ, WeChat, Telegram, Feishu, and Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent host-level services and cron jobs can continue running after installation and may affect the host beyond the agent session.

Mitigation: Install only on a test or dedicated host, review the systemd and crontab changes before enabling them, and require a documented uninstall path before production use.

Risk: Channel patches introduce shell-based execSync calls into message-handling paths.

Mitigation: Do not apply channel patches until command execution paths are reviewed, inputs are validated, and safer process invocation patterns are implemented.

Risk: The skill stores operational state in shared /tmp files, which can be overwritten or read by unrelated local processes.

Mitigation: Move state to a dedicated directory with restrictive permissions before use on shared or multi-user hosts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fanxinyun1991/skills/agent-guardian)
- [Generic Channel Adapter Guide](references/patches/generic.md)
- [QQ Bot Channel Adapter Guide](references/patches/qqbot.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, code snippets, and status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces host-level setup steps, channel patch guidance, watchdog reports, queue summaries, and language-filtered text.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
