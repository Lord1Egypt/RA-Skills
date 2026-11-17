## Description:

Generates Douyin and Dou Store marketing short-video workflows with Volcengine Kickart, including material upload, material and creative analysis, storyboard creation, video generation, and Douyin publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and marketing operators use this skill to turn Douyin or Dou Store product links, plus optional custom media, into structured marketing-video assets and publishing handoff materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Volcengine credentials, private media, logs, and temporary task state.

Mitigation: Use tightly scoped, revocable credentials; avoid sharing long-lived secrets in chat; run only in a trusted workspace; and clear or protect temporary Kickart state and logs after use.

Risk: The configured API base can affect where credentialed requests are sent.

Mitigation: Set ARK_SKILL_API_BASE only from a trusted environment and restrict local workspace or shell access from untrusted users and files.

Risk: Background media-generation tasks may consume credits or expose task and media metadata if repeated or mishandled.

Mitigation: Require explicit user confirmation before paid generation, preserve task IDs for progress checks, and avoid duplicate submissions unless the user asks to regenerate.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-marketing-material-generator)
- [Publisher profile](https://clawhub.ai/user/volcengine-skills)
- [Task Query Guide](references/任务查询指南.md)
- [Creative Analysis Guide](references/创意分析指南.md)
- [Kickart Package Guide](references/套餐开通指南.md)
- [Storyboard Creation Guide](references/故事板创作指南.md)
- [Video Generation Guide](references/消费成片指南.md)
- [Volcengine Authentication Guide](references/火山鉴权指南.md)
- [Material Upload Guide](references/素材上传指南.md)
- [Material Analysis Guide](references/素材分析指南.md)
- [Video Publishing Guide](references/视频发布指南.md)
- [Volcengine IAM key management](https://console.volcengine.com/iam/keymanage)
- [Volcengine Kickart package management](https://console.volcengine.com/kickart/fusion/setting/combobuy?tab=combo)
- [Volcengine Kickart credit recharge](https://console.volcengine.com/kickart/fusion/setting/combobuy?tab=additionalCombo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON result files, video links, and QR-code image paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local task output, media state, logs, video metadata, and publishing QR-code files under temporary Kickart directories.]

## Skill Version(s):

1.1.5 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
