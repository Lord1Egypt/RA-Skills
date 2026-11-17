## Description:

为抖音电商、抖店、商品卡和直播间生成与编辑商品页演示、SKU视频、直播讲解片段及千川投放素材。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, ecommerce operators, video producers, and ad teams use this skill to prepare Douyin ecommerce product-page, SKU-variant, livestream, and Qianchuan ad video generation or editing workflows while preserving approved product facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bearer API keys and uploaded product media may be sent to a configured AI Hive-compatible host.

Mitigation: Use only the intended AI Hive base URL or another trusted compatible endpoint with separate credentials, and review product media and prompts before submission.

Risk: Generated ecommerce videos can include inaccurate SKU details, packaging, claims, prices, promotions, or platform-specific statements if prompts are not reviewed.

Mitigation: Validate outputs against approved SKU facts, packaging, accessories, product claims, and current Douyin ecommerce or advertising rules before publication.

Risk: Local configuration can expose credentials or route requests unexpectedly if reused across environments.

Mitigation: Keep the API key in a restricted user config or environment variable, avoid administrator execution, and verify the configured base URL before running generation commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/douyin-ecommerce-video-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key and chat page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper script can submit AI Hive generation tasks, print task JSON, upload source media, poll status, and download generated image or video files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
