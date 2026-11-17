## Description:

Finds job-relevant agent skills on SkillPicker for a user's task, role, tool, agent, or desired output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geekfoxcharlie](https://clawhub.ai/user/geekfoxcharlie)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to find relevant SkillPicker listings for a user's task, role, tool, agent, or desired output, then check a candidate's linked upstream SKILL.md before recommending it. It does not create skills or assess whether they are safe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install command uses an unpinned CLI version that could change between runs.

Mitigation: Review the CLI package and install command before running it, and use the command only when the user asks to install.

Risk: The security scan had partial coverage because it reported unresolved references.

Mitigation: Check recommendations against their linked upstream SKILL.md and review the skill's instructions and requirements before installing; a listing is not a safety endorsement.

## Reference(s):

- [SkillPicker topic catalog](references/topics.md)
- [SkillPicker](https://skillpicker.xyz/)
- [SkillPicker English skill index](https://skillpicker.xyz/skill-index.en.json)
- [How the SkillPicker index is built](https://skillpicker.xyz/about/)
- [ClawHub release page](https://clawhub.ai/geekfoxcharlie/skills/find-skills-for-the-job)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands]

**Output Format:** [Markdown recommendations with source links; optional npx install command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Gives a few relevance-matched skills; includes an install command only when the user asks to install.]

## Skill Version(s):

1.0.0 (source: frontmatter, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
