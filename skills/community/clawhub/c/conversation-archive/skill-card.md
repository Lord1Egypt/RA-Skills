## Description:

Conversation Archive helps agents archive session conversations into local JSON records with structured summaries for later review and correction workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anfengxiaoguo](https://clawhub.ai/user/anfengxiaoguo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to persist conversation-derived summaries and session metadata so an agent can review prior discussions and correct misunderstandings. Broad deployment needs privacy and file-write controls because it stores conversation-derived content locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic local persistence of conversation-derived content could retain sensitive excerpts.

Mitigation: Require explicit consent, provide disable and delete controls, and implement the documented redaction and retention behavior before broad use.

Risk: Local file-write behavior could write outside the intended archive location.

Mitigation: Validate archive paths, constrain writes to the archive directory, and restrict file permissions.

Risk: The release evidence says privacy, search, and memory-integration behavior is overstated relative to the artifact.

Mitigation: Implement the claimed behavior or remove the claims before relying on the skill for retrieval or memory integration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anfengxiaoguo/skills/conversation-archive)

## Skill Output:

**Output Type(s):** [JSON, Text, Files]

**Output Format:** [JSON archive files with plain text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists local archive and index files.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
