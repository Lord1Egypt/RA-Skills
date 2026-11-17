## Description:

Systematic memory management for long-running AI agents through heartbeat micro-attention, nightly consolidation, weekly reflection, monthly archiving, and yearly wisdom distillation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andrewagrahamhodges](https://clawhub.ai/user/andrewagrahamhodges)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to scaffold and maintain structured long-term memory for OpenClaw agents. It is intended for setting up new memory systems, improving memory quality, and reducing context degradation when MEMORY.md grows too large.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script installs persistent scheduled jobs that can continue modifying long-term memory files after installation.

Mitigation: Run setup with --dry-run first, target a single intended agent, review the cron prompts, and monitor or disable created jobs if behavior is unexpected.

Risk: The memory lifecycle can preserve sensitive personal data or credentials in durable memory files.

Mitigation: Do not store passwords, API keys, tokens, private keys, addresses, or other sensitive personal data in managed memory files; review generated memory changes regularly.

Risk: Unsafe shell command construction in setup behavior could be influenced by local values such as agent IDs, timezones, prompt files, PATH, or files controlled by another process.

Mitigation: Review and fix shell command construction before use in shared or multi-user environments, and avoid --all unless every discovered agent is intentionally in scope.

## Reference(s):

- [Memory Lifecycle Skill Page](https://clawhub.ai/andrewagrahamhodges/skills/agent-memory-lifecycle)
- [Publisher Profile](https://clawhub.ai/user/andrewagrahamhodges)
- [Nightly Sleep Cycle Prompt](references/nightly-prompt.md)
- [Weekly Reflection Prompt](references/weekly-prompt.md)
- [Monthly Deep Clean Prompt](references/monthly-prompt.md)
- [Yearly Wisdom Distillation Prompt](references/yearly-prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python setup and health-check scripts, cron prompts, and generated memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates persistent scheduled memory-maintenance jobs and writes or updates local memory files when setup is run without dry-run.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
