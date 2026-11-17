## Description:

Content Swarm provides a Chinese-language SOP for topic planning, copywriting, cover creation, quality checks, and multi-platform content distribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoshung1981888](https://clawhub.ai/user/gaoshung1981888)

### License/Terms of Use:

MIT-0

## Use Case:

Content operators and marketing teams use this skill to plan, produce, review, archive, and prepare posts for platforms such as Xiaohongshu, WeChat Official Accounts, Douyin, Bilibili, and Kuaishou.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can create persistent local task files and archives.

Mitigation: Restrict writes to a dedicated workspace and sanitize topic-derived path names before file creation.

Risk: The workflow can prepare or initiate public posting to external platforms.

Mitigation: Require explicit human confirmation before any public upload or publication step.

Risk: Declared permissions may not fully reflect the file-write and distribution behavior described by the skill.

Mitigation: Review the skill before installation and align runtime permissions with the actual file-write and network behavior needed.

## Reference(s):

- [Content Swarm ClawHub Skill Page](https://clawhub.ai/gaoshung1981888/skills/content-swarm)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and structured workflow instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose persistent local task files, platform-specific copy, HTML articles, image-cover requirements, video-script requirements, quality checklists, and upload instructions.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
