## Description:

Operate and troubleshoot the AIHealingMe CLI through the npm package (`aihealingmecli`). Use when tasks involve auth/user/audio/plan/chat/emotion/subscription workflows, payload shaping, command diagnostics, and API failure handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bebetterest](https://clawhub.ai/user/bebetterest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate AIHealingMe CLI workflows, shape command payloads, diagnose failures, and verify command coverage for authentication, healing content, chat, emotion, subscription, memory, behavior, and raw API tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned one-shot npm execution could run an unexpected `aihealingmecli` version on sensitive machines.

Mitigation: Use a vetted and pinned `aihealingmecli` version or a trusted global install before running commands.

Risk: CLI workflows can affect billing, credentials, uploads/downloads, raw API requests, memory, behavior, chat, and emotional-health data.

Mitigation: Use least-privilege or test credentials and require explicit human approval before sensitive or mutable operations.

Risk: Command failures or validation errors could lead to incorrect retries or unintended requests.

Mitigation: Inspect `ok`, `error.code`, `error.status`, and `error.issues[]` before retrying, and prefer payload files for complex JSON.

## Reference(s):

- [Command Map](references/command-map.md)
- [Error Playbook](references/error-playbook.md)
- [AIHealingMe](https://aihealing.me/)
- [AIHealingMe API](https://aihealing.me/api)
- [ClawHub Skill Page](https://clawhub.ai/bebetterest/skills/aiheal-cli-operator)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI commands that affect auth, billing, uploads/downloads, raw API requests, memory, behavior, chat, or emotional-health data and should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
