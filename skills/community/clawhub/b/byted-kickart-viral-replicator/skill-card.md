## Description:

Creates Douyin and short-video variations by copying the structure, copy, and style of popular reference videos into similar marketing content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, ecommerce, and content teams use this skill through an agent to collect product materials and a reference video, run Volcengine Kickart workflows, and generate short-form marketing videos with a similar structure and style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential handling is under-scoped and may expose Volcengine access credentials.

Mitigation: Use short-lived, least-privilege credentials; do not paste long-lived AK/SK secrets into chat; rotate any credentials that may have been exposed.

Risk: Existing logs may contain sensitive Authorization data.

Mitigation: Review and remove sensitive logs under /tmp/openclaw/byted-kickart-viral-replicator/logs before reuse or sharing.

Risk: The dynamic update command, detached polling process, and broad local media cache need review before normal use.

Mitigation: Review update commands and background polling behavior before installation, and clear or restrict local media cache locations after each workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-kickart-viral-replicator)
- [Viral replication guide](references/爆款裂变指南.md)
- [Volcengine authentication guide](references/火山鉴权指南.md)
- [Kickart plan and quota guide](references/套餐开通指南.md)
- [Material upload guide](references/素材上传指南.md)
- [Material analysis guide](references/素材分析指南.md)
- [Creative analysis guide](references/创意分析指南.md)
- [Video reference guide](references/视频参考指南.md)
- [Digital avatar guide](references/数字形象指南.md)
- [Task query guide](references/任务查询指南.md)
- [Volcengine virtual avatar compliance commitment](https://www.volcengine.com/docs/6664/2369812?lang=zh)
- [Volcengine compliance commitment](https://www.volcengine.com/docs/6664/2369383?lang=zh)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON task results, status messages, and generated video links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require Volcengine credentials, valid Kickart quota, uploaded media, and asynchronous task polling.]

## Skill Version(s):

1.0.5 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
