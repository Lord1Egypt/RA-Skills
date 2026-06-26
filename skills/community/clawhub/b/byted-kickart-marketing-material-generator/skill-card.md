## Description: <br>
Generates Douyin and Douyin Shop product marketing videos through Volcengine Kickart, including custom media upload, material analysis, creative analysis, storyboard creation, video generation, and Douyin publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volcengine-skills](https://clawhub.ai/user/volcengine-skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External merchants, marketing operators, and their agents use this skill to turn Douyin Shop or Douyin product links and optional uploaded media into short-form marketing video assets and publishing handoff materials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive cloud credentials and may handle authorization headers or request content during execution. <br>
Mitigation: Use least-privilege, non-production credentials where possible, avoid pasting broad access keys into chat, and inspect or redact logs before sharing them. <br>
Risk: The workflow uploads user media to Volcengine/Kickart services and can return generated video links or publishing QR codes in chat. <br>
Mitigation: Use only approved media, verify that the external service is acceptable for the data, and review generated links or QR codes before publishing. <br>
Risk: The skill runs asynchronous tasks, background polling, and account-side actions that can consume service credits or affect publishing workflows. <br>
Mitigation: Track task IDs, confirm user intent before resubmission or publishing, and monitor account usage while the workflow is active. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/byted-kickart-marketing-material-generator) <br>
- [Volcengine authentication guide](artifact/references/火山鉴权指南.md) <br>
- [Package setup and validation guide](artifact/references/套餐开通指南.md) <br>
- [Material upload guide](artifact/references/素材上传指南.md) <br>
- [Material analysis guide](artifact/references/素材分析指南.md) <br>
- [Creative analysis guide](artifact/references/创意分析指南.md) <br>
- [Storyboard creation guide](artifact/references/故事板创作指南.md) <br>
- [Video generation guide](artifact/references/消费成片指南.md) <br>
- [Video publishing guide](artifact/references/视频发布指南.md) <br>
- [Task progress query guide](artifact/references/任务查询指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON result files, video download links, QR code image paths, and user-facing status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Volcengine or ArkClaw credentials, uploads user media to Kickart services, stores task IDs for asynchronous polling, and writes generated artifacts under /tmp/openclaw/kickart/output/.] <br>

## Skill Version(s): <br>
1.1.5 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
