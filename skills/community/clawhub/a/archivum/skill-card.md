## Description:

Operate a Git-backed Archivum as durable agent memory for projects, research, decisions, meetings, tasks, sources, and outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[antreasantoniou](https://clawhub.ai/user/antreasantoniou)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and project teams use this skill to let an agent find, capture, update, connect, audit, and resume durable project memory in a local Archivum workspace. It is useful when work needs source-backed continuity across conversations without treating every Markdown repository as an archive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may update local profile, state, task, decision, research, meeting, and output records that influence future agent work.

Mitigation: Review proposed archive edits before accepting them, especially changes to durable profile, state, task, and decision records.

Risk: Archive records can mix quotations, paraphrases, observations, and inferences if captured carelessly.

Mitigation: Keep source URLs or repository-relative paths with captured material and preserve quotation, paraphrase, observation, and inference as distinct claims.

Risk: Initializing a new Archivum workspace pulls from an external project repository.

Mitigation: Initialize only after explicit user permission and review the target path before creating or cloning workspace files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/antreasantoniou/skills/archivum)
- [Archivum project repository](https://github.com/AntreasAntoniou/archivum)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with repository-relative paths, inline shell commands, and local archive file edits when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill can read and update scoped Archivum records, preserve source links, and propose initialization only with explicit user permission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
