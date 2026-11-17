## Description:

File-based continuity and recovery protocol for OpenClaw, Hermes, and similar agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeremymartinus-pixel](https://clawhub.ai/user/jeremymartinus-pixel)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to help file-backed agents preserve, recover, checkpoint, and restore working context across sessions, model changes, compaction, restarts, and handoffs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory files can persist operating rules and influence future agent actions without strong integrity controls.

Mitigation: Install only in trusted workspaces, restrict write access to trusted parties, and review SESSION-STATE.md, memory/*.md, and MEMORY.md before recovery.

Risk: Saved next steps or standing rules may cause an agent to resume stale or unintended actions.

Mitigation: Require confirmation before adopting standing rules or executing saved next steps, especially in shared projects or sensitive environments.

Risk: Durable memory may expose private or sensitive project context when used in shared chats.

Mitigation: Avoid exposing private memory unless authorized, and do not store secrets in plaintext.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jeremymartinus-pixel/skills/context-memory-recovery)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jeremymartinus-pixel)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown files and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update SESSION-STATE.md, memory/YYYY-MM-DD.md, and MEMORY.md in the workspace.]

## Skill Version(s):

0.2.0 (source: frontmatter, skill.yaml, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
