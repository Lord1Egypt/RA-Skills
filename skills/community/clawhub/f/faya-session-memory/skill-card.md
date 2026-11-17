## Description:

Persistent session memory system that converts OpenClaw session transcripts into searchable Markdown, builds an auto-updating glossary index, and suggests memory-aware cron job prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltbotmolty-del](https://clawhub.ai/user/moltbotmolty-del)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw agent operators use this skill to preserve useful context across compaction by converting prior sessions into searchable local memory, generating a session glossary, and preparing memory-aware cron guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can retain and index sensitive prior conversations as local memory.

Mitigation: Exclude sensitive sessions before conversion, review generated memory files, and add redaction and retention controls before scheduled use.

Risk: Generated glossary entries and extracted decisions may be incomplete or misleading.

Mitigation: Treat glossary decisions as untrusted notes and verify important details against the original session transcript before acting on them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moltbotmolty-del/skills/faya-session-memory)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown files, terminal commands, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local memory transcripts, a session glossary, and a cron optimization report when its scripts are run.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
