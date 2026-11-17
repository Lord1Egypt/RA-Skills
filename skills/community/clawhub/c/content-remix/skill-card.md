## Description:

Chinese content remix tool that transforms one source text into platform-native versions for Xiaohongshu, Douyin, WeChat Official Account, Zhihu, Weibo, and WeChat Video, with platform adaptation rules and advertising-law compliance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

Content marketers, social media operators, and agents use this skill to rewrite Chinese source content into platform-specific posts, scripts, hashtags, calls to action, and distribution guidance. It is intended for multi-platform Chinese content distribution with advertising-law wording checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send unpublished or confidential content to a remote API when using the included script.

Mitigation: Avoid submitting confidential unpublished material unless the user accepts that the remote service will handle it.

Risk: Advertising-law and platform compliance checks are drafting guidance, not legal advice.

Mitigation: Have a qualified human reviewer confirm regulated, medical, financial, education, or advertising claims before publication.

Risk: Platform rules, content lengths, and hashtag practices can change over time.

Mitigation: Verify current platform publishing rules before using generated content in high-impact campaigns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/content-remix)
- [Content Remix API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown sections containing rewritten platform versions, compliance findings, hashtags or topics, word counts, and distribution suggestions; the included shell script returns text from the remote API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored by target platform and may include titles, body copy, calls to action, replacement suggestions, posting-time guidance, and compliance status.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
