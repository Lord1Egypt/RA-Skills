## Description:

AI SkillHub helps an agent extract content from supported URLs, classify the material, generate source-content and skill Markdown files, and publish the result to GitHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eeyan2025-art](https://clawhub.ai/user/eeyan2025-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content curators use this skill to turn web, video, or pasted source material into structured skill documentation and repository-ready files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may publish complete extracted or pasted source material to GitHub.

Mitigation: Use only non-sensitive source material and require explicit confirmation before publishing generated files.

Risk: Local GitHub credentials may be used during automated repository publishing.

Mitigation: Use a narrowly scoped GitHub token and avoid running the workflow with broad or personal credentials.

Risk: Weak URL, keyword, command, and repository-path validation can lead to unsafe or unintended operations.

Mitigation: Validate URLs, generated path components, shell arguments, and repository targets before executing commands.

Risk: Shared temporary paths can expose or overwrite extracted content between runs.

Mitigation: Use secure per-run temporary directories and remove generated working files after review or publishing.

## Reference(s):

- [AI SkillHub on ClawHub](https://clawhub.ai/eeyan2025-art/skills/ai-skillhub)
- [Publisher profile: eeyan2025-art](https://clawhub.ai/user/eeyan2025-art)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce raw extracted content, generated SKILL.md content, classification metadata, and GitHub publishing commands.]

## Skill Version(s):

2.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
