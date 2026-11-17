## Description:

使用 Nano Banana 2 把广告简报变成可测试的广告图片，明确受众、单一主张、视觉证据、品牌资产、CTA 安全区与禁用表述。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, designers, and ad operations practitioners use this skill to turn an advertising brief into AI-generated ad-image candidates with clear audience, claim, visual evidence, brand-asset, CTA safe-zone, and prohibited-expression constraints. It supports new-customer, single-claim proof, brand KV, remarketing, and single-variable creative testing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AI Hive API key and may store it locally in `~/.ai-hive/config.json`.

Mitigation: Use an isolated environment where possible, provide only an AI Hive key appropriate for this workflow, and keep the local config file permissions restricted.

Risk: User-selected reference images are uploaded to AI Hive and its upload/download storage flow.

Mitigation: Use only approved, non-sensitive brand and product images that the team is comfortable sending to AI Hive.

Risk: The documented dependency install uses unpinned `requests`.

Mitigation: Pin and review the `requests` version in managed environments before deployment.

Risk: Generated ad images can contain claims, prices, visual implications, or layout choices that are not suitable for publication.

Mitigation: Have the ad operations team review final copy, prices, compliance statements, brand assets, and placement safe zones before running campaigns.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ad-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline bash commands; the CLI returns JSON task data and downloads generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses fixed model public_model_nano_banana_2 through AI Hive; optional reference images, batch size, routing mode, model parameters, and output directory can be supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
