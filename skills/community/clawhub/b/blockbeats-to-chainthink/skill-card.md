## Description:

Fetches a BlockBeats article from a supplied link, extracts the title, summary, HTML body, and images, and saves it as a ChainThink draft.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dyc0616c-oss](https://clawhub.ai/user/dyc0616c-oss)

### License/Terms of Use:


## Use Case:

Content operators and publishing agents use this skill to turn a BlockBeats article URL into a ChainThink backend draft with extracted article metadata and HTML content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains an embedded ChainThink admin token.

Mitigation: Remove and revoke the embedded token, and require a secure user-provided token at runtime.

Risk: The skill can upload loosely validated web content into ChainThink.

Mitigation: Enforce an exact BlockBeats URL allowlist and sanitize or preview imported HTML before saving.

Risk: The workflow creates a ChainThink draft from fetched content with limited user control.

Mitigation: Ask for explicit confirmation before creating or updating a draft.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dyc0616c-oss/skills/blockbeats-to-chainthink)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and plain text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns ChainThink draft status and article ID when saving succeeds.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
