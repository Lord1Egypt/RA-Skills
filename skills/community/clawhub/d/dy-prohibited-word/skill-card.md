## Description:

检测文案、文件或网页中的抖音违禁词并加粗显示，提供违禁词替换建议和仅替换违禁词后的文案；当接口返回积分不足（code=3210）时，自动唤起支付宝完成充值后继续查询。

This skill is ready for commercial/non-commercial use.

## Publisher:

[if530770](https://clawhub.ai/user/if530770)

### License/Terms of Use:

MIT-0

## Use Case:

Douyin content creators and marketing operators use this skill to check copy, files, or webpages for potentially prohibited terms and receive highlighted findings, contextual replacement suggestions, and a revised copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The recharge workflow can install a payment tool, submit a payment, and retry the query automatically after payment.

Mitigation: Require approval before installing payment tools and before each recharge; verify the recipient and amount, and use a reviewed, pinned payment package.

Risk: Submitted text is sent to RedFox, and revised copies remain on disk despite the skill's privacy claim.

Mitigation: Provide the intended account key explicitly, avoid confidential content unless its processing and storage are acceptable, and review or remove saved copies when no longer needed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/if530770/skills/dy-prohibited-word)
- [RedFox service](https://redfox.hk?source=clawhub)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [Core workflow](references/core_workflow.md)
- [Alipay recharge guidance](references/alipay-recharge.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown findings with highlighted terms and replacement suggestions, plus a plain-text revised copy]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can process pasted text or extracted text from supported files, images, and webpages; revised text is also written to a local text file.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
