## Description:

Organize completed projects into searchable archives with session transcript backup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaigegao1110](https://clawhub.ai/user/kaigegao1110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill after project completion to create private, searchable project archives with transcripts, deliverables, decisions, and reconstruction notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill copies and can retain session transcripts that may contain sensitive project or client data.

Mitigation: Run the sanitizer, manually inspect sanitized transcripts before committing, and keep archives inside the internal workspace unless publication is explicitly approved.

Risk: Transcript selection can fall back to the most recent transcript when no explicit session key is provided.

Mitigation: Require or confirm the session identifier and source path before archiving to avoid copying unrelated session data.

Risk: Deleting source session files is destructive if the wrong files are selected.

Mitigation: Approve deletion only after the exact source files are shown and the sanitized archive copy has been verified.

## Reference(s):

- [Archive Project homepage](https://github.com/KaigeGao1110/ArchiveProject)
- [ClawHub Archive Project skill page](https://clawhub.ai/kaigegao1110/skills/archive-project)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, configuration]

**Output Format:** [Markdown archive files, JSONL transcript copies, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Archives are intended for internal workspace storage and should be sanitized before commit.]

## Skill Version(s):

1.2.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
