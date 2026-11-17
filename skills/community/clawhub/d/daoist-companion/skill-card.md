## Description:

Daoist Companion helps beginners with Daoist classic-text explanations, practice reminders, beginner path planning, meditation basics, and private practice-log templates while refusing ritual, divination, medical, and oral-transmission guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cucmeliu](https://clawhub.ai/user/cucmeliu)

### License/Terms of Use:

MIT

## Use Case:

External users and agent operators use this skill as a beginner-oriented Daoist study and practice companion for classic-text Q&A, practice calendar reminders, guided journaling, and cultural orientation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run Bash and install an unpinned Python calendar package at runtime.

Mitigation: Review the skill before installation and preinstall a pinned calendar dependency in a controlled environment.

Risk: The journal feature may save sensitive religious practice notes under the user's home directory.

Mitigation: Use the journal feature only on a private machine, or modify the workflow to ask before saving and to use a user-selected storage location.

Risk: The skill discusses religious practice topics that include boundaries around ritual, internal alchemy, divination, and health.

Mitigation: Keep the documented refusal boundaries active and direct users to qualified human teachers or medical professionals for those topics.

## Reference(s):

- [Daoist Companion ClawHub Page](https://clawhub.ai/cucmeliu/skills/daoist-companion)
- [Daoist Companion Homepage](https://github.com/cucmeliu/daoist-companion.git)
- [Daoist Classic Texts Library](references/classics.md)
- [Practice System and FAQ](references/practice.md)
- [Daoist Cultural Encyclopedia](references/culture.md)
- [Daoist Practice Quick Reference](references/daoist_knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or write local practice-log files when the user asks to record a journal entry.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
