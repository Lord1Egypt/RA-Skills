## Description:

Generates Chinese platform-specific advertising copy and checks drafts for advertising-law restricted terms through an API-backed compliance workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, copywriters, and agent users use this skill to draft Chinese ads for platforms such as Xiaohongshu, Douyin, WeChat, Baidu, and e-commerce channels, then review flagged wording and safer replacements before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advertising drafts, titles, keywords, and platform information may be sent to a fixed external Tencent Cloud Function endpoint without clear consent or privacy details.

Mitigation: Use only with content that can be shared with that endpoint, and avoid confidential launches, client material, regulated data, or customer information unless the publisher documents data handling and provides consent or local-only controls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/cn-ad-copywriter)
- [Documented compliance API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with Chinese copy variations, compliance reports, replacement suggestions, and optional shell command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a fixed external API endpoint; the artifact describes a free tier of 20 checks per month.]

## Skill Version(s):

2.0.0 (source: server release evidence, released 2026-05-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
