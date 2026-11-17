## Description:

Store and retrieve files through the AIFS.space cloud storage API for cloud persistence and cross-session file syncing, excluding sensitive content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deploydon](https://clawhub.ai/user/deploydon)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to guide agents in listing, reading, writing, patching, deleting, and summarizing files stored in AIFS.space. It is intended for non-sensitive notes, documents, data persistence, and file syncing across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent use of this skill can send file contents to AIFS.space.

Mitigation: Use it only when remote storage is intended and avoid sensitive content.

Risk: The skill enables broad remote read, write, patch, overwrite, and delete actions.

Mitigation: Prefer least-privilege API keys and confirm the target account and path before any write, patch, overwrite, or delete operation.

## Reference(s):

- [AIFS.space service](https://aifs.space)
- [ClawHub skill page](https://clawhub.ai/deploydon/skills/aifs-space)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an AIFS API key and observes a documented 60 requests per minute per key rate limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
