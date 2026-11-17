## Description:

Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[netanel-abergel](https://clawhub.ai/user/netanel-abergel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to automate multi-step browser workflows, inspect accessibility snapshots, select elements by stable refs, manage browser state, and record or debug sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved browser state can contain authentication cookies, tokens, or other session secrets.

Mitigation: Use test or least-privilege accounts where possible, treat saved state files as secrets, and keep them out of repositories and shared artifacts.

Risk: Command-line examples can encourage exposing real credentials in shell history or logs.

Mitigation: Avoid putting real passwords directly in commands; prefer placeholders, secure secret handling, or interactive authentication.

Risk: Browser recordings, screenshots, PDFs, and traces can capture sensitive page content.

Mitigation: Avoid recording sensitive sessions and review generated artifacts before sharing or publishing them.

Risk: A global latest npm install can drift over time or pull unexpected package changes.

Mitigation: Prefer a pinned local install when using the skill in controlled or production-like environments.

## Reference(s):

- [Agent Browser project](https://github.com/vercel-labs/agent-browser)
- [Command reference](references/commands.md)
- [Examples](references/examples.md)
- [ClawHub skill page](https://clawhub.ai/netanel-abergel/skills/ai-pa-browser-clawdbot)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on the agent-browser CLI, including installation, navigation, snapshots, element interaction, waits, sessions, state persistence, screenshots, PDFs, recordings, and debugging.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
