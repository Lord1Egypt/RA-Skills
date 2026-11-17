## Description:

Executes an OpenClaw, Moltbot, and ClawDBot skill-creation workflow that researches standards and examples, compares approaches, and generates structured skill content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill authors use this skill to create or modify OpenClaw, Moltbot, and ClawDBot skills with a research-backed workflow, standardized SKILL.md structure, metadata, security notes, and example usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill-generation requests and research context can be sent to the SkillBoss API when SKILLBOSS_API_KEY is configured.

Mitigation: Avoid submitting secrets, proprietary code, customer data, or private infrastructure details in skill-generation requests.

Risk: Generated skills can inherit unsafe system-prompt, memory, or under-scoped instructions.

Mitigation: Review generated SKILL.md content, metadata, prompts, and examples before installation, publication, or reuse.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alvis-advanced-skill-creator)
- [ClawdBot skills documentation](https://docs.clawd.bot/tools/skills)
- [OpenClaw skills documentation](https://docs.openclaw.ai/tools/skills)
- [SkillBoss API Hub pilot endpoint](https://api.heybossai.com/v1/pilot)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with YAML frontmatter, tree-style file previews, code blocks, and command examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When SKILLBOSS_API_KEY is set, generated skill content may be produced through the SkillBoss API and should be reviewed before use or publication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
