## Description:

Coding style memory that adapts to your preferences, conventions, and patterns for consistent coding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexbingquanxu-cpu](https://clawhub.ai/user/alexbingquanxu-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to store explicitly confirmed coding preferences in local memory and apply them to future code, guidance, and project-structure decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A referenced criteria file contradicts the main skill boundary by mentioning updates to SKILL.md or other skill source files.

Mitigation: Treat local preference files under ~/coding/ as the only allowed storage target and do not update skill source files when recording preferences.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alexbingquanxu-cpu/skills/coding-custom)
- [Skill Homepage](https://clawic.com/skills/coding)
- [Preference Criteria](artifact/criteria.md)
- [Preference Dimensions](artifact/dimensions.md)
- [Memory Templates](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local memory entries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores and reads confirmed coding preferences from local files under ~/coding/.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
