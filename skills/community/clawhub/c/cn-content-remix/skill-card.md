## Description:

cn-content-remix helps agents rewrite Chinese content into platform-native versions for Xiaohongshu, Douyin, WeChat Official Account, Zhihu, Weibo, and WeChat Video, with platform rules and advertising-law checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content marketers, and agent users use this skill to adapt one Chinese source text into channel-specific drafts, scripts, hashtags, and posting guidance for major Chinese social platforms while checking for advertising-law risk terms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a Tencent SCF endpoint for platform-rule lookups and documented content checks.

Mitigation: Install only when this network behavior is acceptable, and review the generated content before publishing.

Risk: Advertising-law checks can miss context-specific or jurisdiction-specific compliance issues.

Mitigation: Treat checks and replacement suggestions as review aids, and manually verify regulated or promotional claims before publication.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/cn-content-remix)
- [Platform rules API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with platform-specific content drafts, compliance notes, tags, posting guidance, and optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a disclosed Tencent SCF endpoint for platform-rule lookups, and may call the documented compliance-check API if the agent chooses to use it.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
