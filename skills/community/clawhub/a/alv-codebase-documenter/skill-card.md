## Description:

This skill helps agents write documentation for codebases, including README files, architecture documentation, code comments, and API documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alvisdunlop](https://clawhub.ai/user/alvisdunlop)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to create beginner-friendly project documentation, architecture guides, API docs, and explanatory code comments from a codebase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact requires SKILLBOSS_API_KEY and describes AI-powered documentation generation through SkillBoss API Hub, but the artifact does not explain what codebase data is sent there.

Mitigation: Use the skill only when the external integration is acceptable for the codebase, and review generated documentation before committing it.

Risk: Generated documentation can be incomplete, inaccurate, or misleading if the codebase is complex or the agent misses context.

Mitigation: Review generated README, architecture, API, and code-comment content against the source code before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alvisdunlop/skills/alv-codebase-documenter)
- [Publisher profile](https://clawhub.ai/user/alvisdunlop)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown, prose guidance, templates, and code-comment examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May rely on SKILLBOSS_API_KEY for AI-powered documentation generation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
