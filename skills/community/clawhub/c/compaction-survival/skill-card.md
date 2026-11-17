## Description:

Prevent context loss during LLM compaction via Write-Ahead Logging (WAL), Working Buffer, and automatic recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rustyorb](https://clawhub.ai/user/rustyorb)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to preserve exact task state, decisions, preferences, paths, values, and recovery notes across context-window compaction during long-running sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist names, paths, URLs, IDs, preferences, decisions, and whole messages in local memory files without clear consent or retention limits.

Mitigation: Use explicit opt-in, redact sensitive content, apply retention limits, and scope recovery files to the active task; avoid use around secrets, credentials, regulated personal data, confidential customer data, or shared workspaces unless those controls are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rustyorb/skills/compaction-survival)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown guidance with file paths and procedural checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts the agent to maintain local session-state and working-buffer files for compaction recovery.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
