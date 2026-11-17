## Description:

Set up, inspect, or maintain a local user-preference memory shared across coding agents such as Codex and Claude Code. Use only when the user explicitly asks to remember a preference, review or forget stored preferences, configure Dongwo lifecycle hooks, or maintain an existing Dongwo installation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cutd](https://clawhub.ai/user/cutd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers using coding agents such as Codex or Claude Code can use Dongwo to set up and maintain a shared local memory of preference summaries. Hook setup is opt-in, and saved summaries can be reviewed or removed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved preference excerpts may contain private text, including the entirety of a short prompt.

Mitigation: Enable hooks only if automatic local retention is acceptable; review the ledger and generated archive periodically, and remove hook configuration to stop collection.

Risk: Secret filtering is imperfect and cannot guarantee that sensitive text is never retained.

Mitigation: Do not rely on filtering to protect secrets; inspect stored summaries and preview deletions before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cutd/skills/dongwo)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup and lifecycle actions are opt-in; destructive maintenance requires confirmation.]

## Skill Version(s):

1.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
