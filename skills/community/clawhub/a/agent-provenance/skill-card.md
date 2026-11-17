## Description:

Tracks authorship, review dates, and changes to OpenClaw instruction and memory files so users can audit agent-maintained workspace guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richgoodson](https://clawhub.ai/user/richgoodson)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to review file authorship, identify stale instructions and memory topics, and inspect changes to agent-maintained workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and modify important instruction and memory files, including AGENTS.md, USER.md, and MEMORY.md.

Mitigation: Review proposed changes and git diffs before accepting updates to workspace guidance.

Risk: An optional weekly check can post recurring reports to the conversation.

Mitigation: Enable scheduling only with explicit consent and disable the job if reports are no longer wanted.

## Reference(s):

- [Agent Provenance on ClawHub](https://clawhub.ai/richgoodson/skills/agent-provenance)
- [Publisher profile on ClawHub](https://clawhub.ai/user/richgoodson)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports, file provenance headers, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can update workspace documentation when asked; recurring reports require explicit opt-in.]

## Skill Version(s):

2.3.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
