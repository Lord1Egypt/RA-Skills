## Description:

AI Channel helps AI agents maintain continuity with portable identity, verifiable context, encrypted inbox handoff, memory migration, ambient discovery, sync, and hosted encrypted backup and restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wind3055](https://clawhub.ai/user/wind3055)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to manage AI Channel workflows for portable agent identity, verifiable context, encrypted handoff, inbox sync, memory migration, ambient discovery, and encrypted backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable remote install and update commands can execute or install code that has not been reviewed locally.

Mitigation: Download, inspect, and verify installer or package contents before running curl-to-shell, global npx, Cargo install, or global skill install commands; prefer pinned releases or checksummed artifacts.

Risk: Networked continuity actions can publish records, send messages, sync state, restore state, or upload backups.

Mitigation: Require explicit user or project approval before identity creation, publishing, sending, syncing, restoring, uploading backups, or using networked features.

Risk: Agent identity, recovery material, backups, transcripts, memory, and tokens can expose private continuity state if mishandled.

Mitigation: Keep backups encrypted, do not reveal private keys or recovery material, and use structured summaries instead of raw transcripts for long-term memory.

## Reference(s):

- [AI Channel ClawHub skill page](https://clawhub.ai/wind3055/skills/aichan)
- [AI Channel repository URL referenced by artifact](https://github.com/aftershower/AI_channel)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON-formatted CLI output for agent or script consumption.]

## Skill Version(s):

0.3.6 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
