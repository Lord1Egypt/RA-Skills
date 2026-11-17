## Description:

Self-learn to decide when to act, when to ask, and which actions should always need approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help an agent maintain a durable ask-vs-act policy across sessions, especially for proactive drafting, editing, research, and local work. It guides the agent to act on low-risk reversible work while escalating external, irreversible, financial, legal, credential, deletion, deployment, or third-party-impacting actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local notes can influence future agent decisions.

Mitigation: Review the ~/escalate files periodically and keep hard boundaries explicit.

Risk: Workspace AGENTS or SOUL snippets can influence future agent behavior if approved without review.

Mitigation: Review the exact snippet before approval; setup guidance requires explicit approval and non-destructive edits.

Risk: Local memory could accidentally retain sensitive information.

Mitigation: Do not persist credentials, secrets, or copied third-party private data in escalation memory.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/escalate)
- [Declared Homepage](https://clawic.com/skills/escalate)
- [Setup Guide](artifact/setup.md)
- [Hard Boundaries](artifact/boundaries.md)
- [Pattern Recognition](artifact/patterns.md)
- [Memory Template](artifact/memory-template.md)
- [Migration Guide](artifact/migration.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local escalation notes under ~/escalate when used by an agent with filesystem access.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
