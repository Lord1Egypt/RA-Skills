## Description:

Use when setting up or improving an agent memory workflow for OpenClaw, Codex, or Obsidian with MEMORY.md, daily notes, session recovery, and optional OpenViking support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjke84](https://clawhub.ai/user/cjke84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to set up a local-first memory workflow with recovery files, daily notes, Obsidian archiving, and optional recall backends. It is intended for OpenClaw, Codex, and related agent workspaces that need portable memory practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup import and export can restore or archive more workspace files than users reasonably expect.

Mitigation: Inspect backup contents before restoring, do not import archives from untrusted sources, avoid symlinks inside memory and attachments, and keep a separate backup before using clean restore mode.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjke84/skills/agent-memory-system-guide)
- [Project homepage](https://github.com/cjke84/agent-memory-system-guide)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw memory_search documentation](https://docs.openclaw.ai/tools#memory_search)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands, file templates, and optional JSON or Markdown report output from helper commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Helper commands may create local memory files, Markdown reports, and backup zip archives when executed by the user or agent.]

## Skill Version(s):

1.1.7 (source: release evidence and manifest.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
