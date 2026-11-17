## Description:

Digital Life Grandpa Skill guides users through a 5-step interview and 7-layer modeling process to generate a personalized grandpa companion skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafaelsachetto-lang](https://clawhub.ai/user/rafaelsachetto-lang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to collect family memories through a structured interview and turn them into a personalized grandpa-themed companion skill for remembrance, comfort, and family storytelling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and persist intimate family memories, interview answers, photos, logs, and details about living relatives.

Mitigation: Treat interview answers as sensitive personal data; persist or share them only with clear consent, exclude private artifacts from publication, and define a deletion plan.

Risk: The included GitHub upload helper can publish the skill directory publicly, including generated memories or local configuration if they are present.

Mitigation: Inspect exactly what will be committed before running the script, prefer a private repository, and remove generated memories, photos, logs, secrets, and local configuration.

Risk: Generated companion content may unintentionally distort or overstate a relative's wishes, memories, or personal history.

Mitigation: Review generated content with the family before use, preserve uncertainty, and avoid adding claims that were not provided in the interview.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rafaelsachetto-lang/skills/digital-life-grandpa-skill)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with interview prompts, generated skill templates, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce family-memory files and companion-skill instructions when users provide interview answers.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter version is 6.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
