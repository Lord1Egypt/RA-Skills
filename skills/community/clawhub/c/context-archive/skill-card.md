## Description:

User-driven conversation archiving for AI agents. Archive by topic or time, free context, recall on demand.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaszhou22](https://clawhub.ai/user/thomaszhou22)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users use this skill to summarize selected conversation segments into workspace-local Markdown archives, list saved archives, and recall archived summaries into the current agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Conversation summaries may be saved locally under archives/ and can preserve sensitive details if the user chooses to archive them.

Mitigation: Archive only information intended to remain on disk, avoid secrets or private data, and periodically review or delete archive files that are no longer needed.

## Reference(s):

- [OpenClaw](https://github.com/openclaw/openclaw)
- [ClawHub skill page](https://clawhub.ai/thomaszhou22/skills/context-archive)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Conversational text and structured Markdown archive files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates, lists, and reads workspace-local files under archives/ when invoked by the user.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
