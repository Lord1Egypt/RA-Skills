## Description:

Helps developers create, improve, audit, consolidate, and clarify agent skills using a structured workflow and evaluation tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[j-levee](https://clawhub.ai/user/j-levee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill creators use this skill to build or upgrade agent skills, assess their quality, consolidate overlapping skills, and improve how clearly agents can use them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The session hook can contact cloud endpoints with a persistent anonymous ID even when cloud sync is documented as off.

Mitigation: Review network behavior before installation; disable the session hook if unwanted, or require explicit cloud opt-in before any signal download.

Risk: Local method-level telemetry files are created by default.

Mitigation: Check local recording settings and disable collection if it does not meet your privacy requirements.

Risk: Forge and publication tools can inspect local skill directories and interact with cloud services.

Mitigation: Review the directories and cloud actions involved, and approve any release only after checking generated content and sensitive data.

## Reference(s):

- [Skill Forge release on ClawHub](https://clawhub.ai/j-levee/skills/cjg-skill-forge)
- [Forge pipeline](artifact/references/pipeline.md)
- [Skill review rubric](artifact/references/skill-review-rubric.md)
- [Signal and cloud configuration](artifact/references/cloud-config-schema.md)

## Skill Output:

**Output Type(s):** [Markdown guidance, Code, Configuration, Shell commands, Analysis]

**Output Format:** [Markdown reports and guidance, skill files, and configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce skill assessments and plans; review generated files before use or publication.]

## Skill Version(s):

3.2.0 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
