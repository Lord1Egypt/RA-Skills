## Description:

Safely write or update large files over 5000 bytes by reading, incrementally editing small sections, verifying after each step, and using backups for recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ykaixu](https://clawhub.ai/user/ykaixu)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill when creating or modifying large files that may exceed single-operation write limits. It guides incremental edits, verification, fallback strategies, and recovery steps for safer file changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: File modification guidance can still lead an agent to apply incorrect or destructive edits if proposed changes are not reviewed.

Mitigation: Review proposed file edits, verify changed sections after each operation, and use backups for important files.

Risk: Large write operations may be truncated or leave files incomplete.

Mitigation: Prefer incremental edits, keep changes small, and verify file size and ending content after each operation.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No generated files by default; the skill provides workflow guidance for file edits and verification.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
