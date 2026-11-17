## Description:

Automatically analyzes messages for important information, filters noise, and stores meaningful content in memory files without manual remember-this commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[init-v](https://clawhub.ai/user/init-v)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to passively curate long-term agent memory from conversation content, including facts, decisions, preferences, ideas, learnings, project updates, goals, errors, and commitments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill silently persists information from every message into long-term agent files with limited user control.

Mitigation: Install only where passive long-term memory is intended, avoid use around confidential or regulated information, and review memory files regularly.

Risk: Conversation content may include preferences, decisions, project status, tasks, or other sensitive context that should not be retained.

Mitigation: Use the documented override phrases to prevent or clear storage, and calibrate what the skill captures during periodic memory reviews.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/init-v/skills/auto-memory-curation)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown memory entries appended to agent memory files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs silently on each message and uses append-only memory updates unless disabled or adjusted by the user.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
