## Description:

Adds required header metadata to newly created SKILL.md files after skill creation workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quntion](https://clawhub.ai/user/quntion)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill after creating a new skill to add or update Author, Date, and BusinessSupportVersion metadata in the new SKILL.md.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may automatically update SKILL.md metadata when a new skill is created, which can surprise users who want manual control over skill headers.

Mitigation: Review the trigger wording and require confirmation before metadata edits when manual control is needed.

## Reference(s):

- [ClawHub Skill Release](https://clawhub.ai/quntion/skills/ai-skill-creator-attach-info)
- [ClawHub Publisher Profile](https://clawhub.ai/user/quntion)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and YAML frontmatter fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May edit SKILL.md metadata fields when triggered after skill creation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
