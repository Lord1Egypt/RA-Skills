## Description:

Guide for creating and importing skills. Use when users need to create or import skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennethchiu2008-fran](https://clawhub.ai/user/kennethchiu2008-fran)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to create, package, review, import, and register agent skills with supporting documentation and helper scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The ZIP extraction helper can write outside the intended extraction folder.

Mitigation: Review and fix path validation before using the extraction helper on ZIP archives, and only process packages from trusted sources.

Risk: The registration helper persistently copies skills into the user's EasyClaw skills directory.

Mitigation: Confirm the source folder and user approval before registration, and review the copied skill before enabling it.

Risk: Imported skill content could contain unsafe, unethical, legally problematic, or malicious instructions.

Mitigation: Perform the documented security, ethical, and legal review before importing or registering a skill.

## Reference(s):

- [Progressive Disclosure](references/progressive-disclosure.md)
- [Skill Structure](references/skill-structure.md)
- [Good Skill Examples](references/examples.md)
- [Skill Writing Best Practices](references/best-practices.md)
- [ClawHub skill page](https://clawhub.ai/kennethchiu2008-fran/skills/create-skill)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or use helper scripts for ZIP extraction and local EasyClaw skill registration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
