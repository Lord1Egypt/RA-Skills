## Description:

Chinese SEO Compliance helps agents scan Chinese marketing content for advertising-law, banned-word, sensitive-word, platform-rule, and SEO issues across Baidu, Douyin, Xiaohongshu, Taobao, WeChat, and Bilibili.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lm203688](https://clawhub.ai/user/lm203688)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, marketers, and content teams use this skill to check Chinese-language advertising and SEO content before publication. It guides platform selection, API-based scanning, severity review, suggested wording fixes, and re-scan verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the workflow pushes user content to an unaudited external API without clear consent or privacy details.

Mitigation: Review the external service and its data-handling terms before use, and avoid sending confidential drafts, customer data, credentials, personal data, or regulated material unless that review is acceptable.

Risk: Compliance checks can miss changing legal or platform requirements and do not guarantee legal safety.

Mitigation: Use the scan as a pre-publication aid and require legal or qualified human review for high-risk, regulated, or commercially material content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lm203688/skills/chinese-seo-compliance)
- [Hosted web app](https://1341839497-jv04655vcs.ap-shanghai.tencentscf.com/)
- [Compliance check API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com/check)
- [Suggestions API endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com/suggestions?platform=xiaohongshu)
- [API health endpoint](https://1341839497-2yuxt6z58d.ap-guangzhou.tencentscf.com/health)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls]

**Output Format:** [Markdown with inline shell commands and JSON API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include platform-specific violation summaries, severity notes, suggested replacements, SEO suggestions, and re-scan outcomes.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
