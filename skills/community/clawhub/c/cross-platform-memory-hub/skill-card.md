## Description:

Cross-platform persistent memory system for AI agents: session continuity, task tracking, decision records, and project context across coding sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinyu12166](https://clawhub.ai/user/jinyu12166)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure a cross-platform memory workflow, create task and decision records, and coordinate Obsidian-backed session context across OpenClaw, Codex, and Claude Code. Paid use enables memory synchronization authorization through clawtip verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary marks the package as suspicious and says its payment and authorization workflow requires review before installation.

Mitigation: Review the payment flow before use and install only when the user accepts the clawtip-based paid access model.

Risk: Order creation stores local order/payment metadata and can include the user's question in the order record.

Mitigation: Avoid placing secrets or sensitive project details in payment questions and remove local order records when they are no longer needed.

Risk: Memory workflows can read from or write to a local Obsidian vault if enabled by the user.

Mitigation: Require explicit user confirmation of read/write scope, target paths, and summaries before accessing or modifying local notes.

Risk: The security guidance says not to rely on this package as a fully implemented cross-platform memory sync system without additional controls.

Mitigation: Treat synchronization claims as requiring operational validation and add access, logging, and review controls before depending on it for critical work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinyu12166/skills/cross-platform-memory-hub)
- [README](README.md)
- [Obsidian Initialization Guide](config/obsidian-init.md)
- [OpenClaw Usage Guide](adapters/openclaw/usage-guide.md)
- [Codex Project Rules](adapters/codex/project-rules.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command snippets, JSON status lines, and local file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Chinese-language interaction guidance, adapter configuration instructions, local order/payment metadata, and Obsidian-oriented templates.]

## Skill Version(s):

1.0.25 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
