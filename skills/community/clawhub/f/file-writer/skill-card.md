## Description:

Safely write or update large files over 5000 bytes by reading current state, editing incrementally, verifying each change, and using fallback recovery methods.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to guide safer large-file creation and updates, especially when direct writes may truncate content or corrupt files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to read and modify files the user asks it to work on, including sensitive or important files.

Mitigation: Review requested edits, use backups for critical files, and verify file contents after each incremental change.

Risk: Large or imprecise edits can still truncate, corrupt, or misplace content if the target text is not matched carefully.

Mitigation: Read the current file state first, keep changes small, match replacement text exactly, and validate the final file after edits.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Procedural file-editing strategy; no API calls or external services are described.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
