## Description:

生成与编辑抖音短视频封面、抖音电商商品卡封面和巨量千川素材首图，支持参考图、批量方向和 AI Hive 任务下载。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, merchants, and marketing teams use this skill to turn a video topic or product selling point into vertical Douyin cover concepts and generated image outputs for feeds, product cards, campaign tests, or profile series.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent API credentials and configurable AI Hive base URLs can expose sensitive access if the service, publisher, or endpoint is not trusted.

Mitigation: Install only from a trusted publisher, keep AI_HIVE_API_KEY scoped and revocable, and avoid custom AI_HIVE_BASE_URL or --base-url values unless independently verified.

Risk: Downloaded files and API responses influence local writes in the selected output directory.

Mitigation: Run the skill in a contained environment and set a dedicated --output-dir before downloading generated assets.

Risk: Generated cover images may contain incorrect Chinese text, altered product details, or unsupported promotional claims.

Mitigation: Manually review title text, product packaging, brand elements, prices, claims, and platform marks before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/douyin-viral-cover-image-generation)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and generated image files downloaded by the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May upload reference images, submit AI Hive generation tasks, poll task status, and write downloaded image files to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
