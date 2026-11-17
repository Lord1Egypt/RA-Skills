## Description:

This skill helps agents plan and produce Xiaohongshu and WeChat content workflows, including topic discovery, article drafts, card-image prompt suggestions, and publishing schedules.

This skill is for research and development only.

## Publisher:

[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo)

### License/Terms of Use:

Personal Use Only License v1.0

## Use Case:

Individual creators and developers use this skill to structure Xiaohongshu or WeChat content production, from collecting material and prioritizing topics to drafting copy, planning card images, and organizing a publishing calendar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions ask users to run an unpinned external project with Docker and npm.

Mitigation: Review the upstream repository, Docker Compose file, npm scripts, dependency lockfiles, and container images, then pin a reviewed commit or release before running it.

Risk: Administrator credentials, API keys, or account-connected publishing credentials may be exposed or stored during setup and use.

Mitigation: Use an isolated development environment, avoid putting administrator passwords on the command line, and do not add real API keys or publishing credentials until data handling is understood.

Risk: Generated social content or publishing plans may be inaccurate, misleading, or unsuitable for publication.

Mitigation: Human-review generated topics, copy, image prompts, and schedules before publishing or sharing them externally.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zmy1006-sudo/skills/ai-content-xiaohongshu)
- [CheeMao ai-content project reference](https://github.com/CheeMao/ai-content)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with prompts, outlines, schedules, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include topic priorities, article structures, Xiaohongshu copy, image prompt suggestions, and publishing plans.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
