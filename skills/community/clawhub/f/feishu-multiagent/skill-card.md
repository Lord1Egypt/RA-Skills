## Description:

Configure OpenClaw multi-agent routing for Feishu multi-account setups with isolated agents, workspace prompts, MEMORY bootstrap, memory embedding checks, routing validation, and common Feishu troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tinywatermonster](https://clawhub.ai/user/tinywatermonster)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to create or repair OpenClaw routing for multiple Feishu bot accounts, keep each account bound to the intended isolated agent, and verify routing, memory, pairing, and channel health before relying on the setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes steps that read and persist local API credentials while configuring Feishu accounts and memory embedding providers.

Mitigation: Review credential-handling steps before use, prefer a secret store or credential reference where supported, avoid shell tracing or session recording, protect OpenClaw configuration backups, and rotate provider keys if they may have appeared in logs, process records, or copied config files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tinywatermonster/skills/feishu-multiagent)
- [OpenRouter API endpoint](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes changed files and key fields, validation command outputs, routing evidence, memory status or indexing evidence, and residual warnings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
