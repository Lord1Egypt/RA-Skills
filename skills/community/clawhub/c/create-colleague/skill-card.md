## Description:

Distills a colleague into an AI Skill by collecting workplace materials and generating Work Skill and Persona content that can evolve over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifeiwang1981](https://clawhub.ai/user/yifeiwang1981)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and developers use this skill to turn a colleague's workplace materials and descriptive input into a reusable Work Skill and Persona skill, then update it as new materials or corrections arrive.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can collect and store private workplace communications and personal materials.

Mitigation: Install and use it only with explicit authorization from the organization and the people whose communications may be processed.

Risk: Credentialed collectors and browser-session access can expose tokens, credentials, or session data.

Mitigation: Use narrowly scoped read-only credentials, avoid the example.com OAuth redirect, and review credential handling before collection.

Risk: Generated persona instructions may persistently misrepresent a person or encode sensitive behavioral assumptions.

Mitigation: Review every generated skill before enabling it and avoid private-chat, raw screenshot, or identity-cloning use cases without documented consent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yifeiwang1981/skills/create-colleague)
- [README](artifact/README.md)
- [Install Guide](artifact/INSTALL.md)
- [Product Requirements](artifact/docs/PRD.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown skill files, JSON metadata, and command-oriented setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent colleague skills that should be reviewed before enabling.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
