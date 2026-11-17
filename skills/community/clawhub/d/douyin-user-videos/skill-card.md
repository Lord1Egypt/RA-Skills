## Description:

获取抖音博主的视频列表。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanshiyang](https://clawhub.ai/user/tanshiyang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to retrieve a Douyin creator's profile video list from a homepage URL, including video descriptions and publish times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill forwards a Douyin login cookie and API key to a third-party service endpoint.

Mitigation: Install only when the publisher and xueai-portal service are trusted with those credentials, and rotate or revoke the cookie and API key if exposure is suspected.

Risk: The DOUYIN_API_URL environment variable can redirect requests to another endpoint.

Mitigation: Set DOUYIN_API_URL only to destinations the user controls or explicitly trusts; otherwise leave the default endpoint unchanged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanshiyang/skills/douyin-user-videos)
- [Douyin cookie and API key setup guide](https://my.feishu.cn/wiki/HbTpwSDMMiu4mUkCsjwcXgCWn7Z)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON tool result with success status, message, count, and video records that agents can summarize as text or markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Douyin profile URL and configured DOUYIN_API_KEY; DOUYIN_COOKIE is optional but may be needed for authenticated access.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
