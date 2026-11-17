## Description:

Writes and corrects English so it reads naturally for the user's intended variety, register, audience, and context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to rewrite, correct, and explain English across spelling varieties, registers, business communication, learner errors, idioms, pronunciation, and writing practice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically builds and reuses persistent local notes about writing preferences, recurring mistakes, contacts, meetings, and projects.

Mitigation: Review the configured local data paths before installation and audit generated notes periodically, especially shared contact and project files.

Risk: User-provided text may contain secrets or sensitive personal details that could be saved into local notes.

Mitigation: Follow the skill's secret-redaction rule and store only pointers to credentials or one-time links, not the secret values themselves.

## Reference(s):

- [ClawHub English Skill Page](https://clawhub.ai/ivangdavila/skills/english)
- [Clawic English Skill Page](https://clawic.com/skills/english)
- [English Skill Source](artifact/SKILL.md)
- [Working File Templates](artifact/memory-template.md)
- [Business English Reference](artifact/business.md)
- [Learner Error Reference](artifact/learners.md)
- [Varieties Reference](artifact/varieties.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown or plain text with optional local note updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write local memory, contact, project, and style notes under configured user paths.]

## Skill Version(s):

1.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
