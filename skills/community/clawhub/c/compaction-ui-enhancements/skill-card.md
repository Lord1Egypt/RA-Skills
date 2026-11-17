## Description:

Background memory compaction with auto-trigger, chat summary paragraph, configurable threshold, model selector, settings tab, and result storage for OpenClaw Control UI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add configurable manual and automatic chat memory compaction, background status toasts, compaction settings, model selection, and optional result review to the OpenClaw Control UI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic compaction can send chat session content to an LLM in the background.

Mitigation: Review the setting before installation and disable auto-compaction for chats containing secrets, proprietary code, personal data, or regulated information.

Risk: Stored compaction summaries may preserve sensitive conversation details in local plaintext.

Mitigation: Keep result storage disabled for sensitive sessions and ensure the agent directory has owner-only filesystem permissions.

Risk: Custom compaction models may use provider credentials and auth paths configured for the agent.

Mitigation: Select compaction models only after confirming the intended provider, credential source, and fallback behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maverick-software/skills/compaction-ui-enhancements)
- [auto-compaction.ts](references/auto-compaction.ts)
- [chat-filters.diff.md](references/chat-filters.diff.md)
- [compact-summary-injection.ts](references/compact-summary-injection.ts)
- [compaction-rpc.ts](references/compaction-rpc.ts)
- [compaction-settings-view.ts](references/compaction-settings-view.ts)
- [context-gauge-ui.diff.md](references/context-gauge-ui.diff.md)
- [sessions-compact-rpc.diff.md](references/sessions-compact-rpc.diff.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces UI and RPC implementation guidance for OpenClaw compaction behavior; optional stored summaries may omit summary text when result storage is disabled.]

## Skill Version(s):

2.3.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
