## Description:

This skill helps agents prepare and publish Markdown blog articles across CSDN, 51CTO, CNBlogs, and Juejin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lainxxx](https://clawhub.ai/user/lainxxx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content authors use this skill to select a posting template, confirm title, tags, body, and target platforms, and coordinate multi-platform publication of Markdown articles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential checks can expose real platform cookies if secret values are printed during inspection.

Mitigation: Change credential checks to verify variable presence without printing values, and redact secrets in any diagnostic output.

Risk: Publishing commands can execute unintended shell input when user-provided title, tags, or content are interpolated directly.

Mitigation: Review generated commands before execution and pass user content through safe argument handling instead of raw shell interpolation.

Risk: The skill can publish live posts to external platforms with authenticated accounts.

Mitigation: Confirm each target platform and draft-versus-publish mode with the user before any live posting command runs.

Risk: Referenced scripts, templates, and platform guidance are required for dependable publishing behavior but are not present in the artifact evidence.

Mitigation: Supply and review the missing scripts, templates, and references before installing or using the skill with real accounts.

## Reference(s):

- [Server-resolved GitHub import](https://github.com/lainXXX/blog-auto-poster-skill)
- [ClawHub skill page](https://clawhub.ai/lainxxx/skills/blog-auto-poster-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash command blocks and a final status summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a temporary Markdown file for user review before or during publishing.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
