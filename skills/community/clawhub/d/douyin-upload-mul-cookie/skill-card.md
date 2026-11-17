## Description:

Automates local Playwright-based video publishing to Douyin, including cookie profile management, metadata entry, optional cover selection, scheduling, and guarded platform authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuhongfeii2](https://clawhub.ai/user/xuhongfeii2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide local Douyin Creator Center publishing workflows from an agent, including cookie capture or validation, video upload, title and tag entry, cover handling, optional scheduling, and platform authorization.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Chanjing platform credentials and Douyin session cookie JSON files.

Mitigation: Treat those values like passwords, keep them out of shared folders and source control, and rotate any credentials that may have been exposed.

Risk: The default platform API URL is plaintext HTTP and publish flows can deduct configured platform points.

Mitigation: Use the skill only with a trusted EasyClaw/Chanjing platform endpoint, prefer an HTTPS CHANJING_PLATFORM_BASE_URL, and confirm point deduction expectations before publishing.

Risk: The automation can publish or schedule content to a live Douyin account.

Mitigation: Validate the selected cookie profile, video, title, tags, cover, schedule time, and target account before running the publish command.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xuhongfeii2/skills/douyin-upload-mul-cookie)
- [Douyin Creator Center](https://creator.douyin.com/)
- [Douyin Creator Center upload page](https://creator.douyin.com/creator-micro/content/upload)
- [Chanjing platform key portal](http://easyclaw.bar/shuziren/user)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create local Douyin cookie JSON files and publish logs; publishing can upload videos, deduct configured platform points, and report success or failure to the platform.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
