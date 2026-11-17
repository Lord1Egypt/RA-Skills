## Description:

Injects recent conversations from Telegram and Discord into the OpenClaw gateway session context so an agent can maintain continuity across OpenClaw channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dq-stack](https://clawhub.ai/user/dq-stack)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to provide an OpenClaw agent with recent cross-platform conversation context from Telegram, Discord, and local memory files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically adds chat logs and local memory files to future prompts, which can expose sensitive context or content from the wrong user, session, or channel.

Mitigation: Deploy only in a tightly controlled single-user environment unless the skill is revised to select memory by verified user, session, and channel with explicit opt-in for each source.

Risk: Recalled conversation content may include prompt-injection-like text or untrusted instructions.

Mitigation: Redact or filter sensitive and prompt-injection-like content before use, preserve sender provenance, and avoid placing recalled content in the system role.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dq-stack/skills/cross-platform-memory)
- [memory-bridge.ts](references/memory-bridge.ts)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with TypeScript code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a memory context string assembled from local memory files and recent Telegram and Discord user messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
