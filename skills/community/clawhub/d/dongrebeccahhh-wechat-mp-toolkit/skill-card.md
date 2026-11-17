## Description:

Helps WeChat public account operators create articles, generate cover images, analyze trending topics, and publish drafts through WeChat publishing workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongrebeccahhh-boop](https://clawhub.ai/user/dongrebeccahhh-boop)

### License/Terms of Use:

MIT-0

## Use Case:

External content operators and developers use this skill to draft WeChat public account articles, generate cover assets, analyze trending topics, and create WeChat drafts for review and publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled WeChat credentials may expose an account or encourage users to run the skill with unsafe secrets.

Mitigation: Do not run with bundled credentials; rotate any matching credentials and provide secrets through the runtime environment or a private local config.

Risk: The one-click workflow can create WeChat drafts and upload media without a clear dry-run or confirmation step.

Mitigation: Add and use a dry-run or explicit confirmation step before network publishing, and review generated content and target account details before submission.

Risk: Cover generation invokes local shell commands and an external cover-generator script path.

Mitigation: Remove or integrity-check the external script dependency, validate file paths and image inputs, and run the workflow with least-privilege filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongrebeccahhh-boop/skills/dongrebeccahhh-wechat-mp-toolkit)
- [Skill definition](artifact/SKILL.md)
- [Quick start README](artifact/README.md)
- [WeChat API endpoint](https://api.weixin.qq.com)
- [Sina News source](https://news.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown articles, generated image files, JSON configuration, and shell-command workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local article and cover files and can submit WeChat drafts when configured with valid credentials.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
