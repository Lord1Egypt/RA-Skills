## Description:

CreBee Social Media Gateway helps an agent manage connected Chinese social media accounts, publish video/image/article content, retrieve publishing status, and access platform analytics through the local CreBee desktop API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzygithub](https://clawhub.ai/user/hzygithub)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to let an agent prepare authenticated CreBee API requests for account lookup, multi-platform content publishing, task cancellation, publishing records, and audience or performance analytics. It is intended for authorized operation of real social accounts connected through the user's CreBee desktop client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide broad posting and cancellation actions for real social media accounts.

Mitigation: Confirm the target account, platform, content, schedule, and task ID with the user before any publish or cancel action.

Risk: The skill uses local media paths for upload workflows.

Mitigation: Verify that each local file path points to the intended media before sending a publish request.

Risk: Bearer tokens, account IDs, revenue data, and audience or fan analytics are sensitive.

Mitigation: Avoid exposing tokens or account identifiers in generated artifacts, logs, or shared messages, and treat analytics as private account data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzygithub/skills/crebee-agent-skill-v1-9-9)
- [CreBee website](https://www.crebee.cn)
- [CreBee download page](https://www.crebee.cn/#/download)
- [Publishing guide](artifact/references/publishing.md)
- [Douyin API](artifact/references/platforms/douyin.md)
- [Bilibili API](artifact/references/platforms/bilibili.md)
- [Xiaohongshu API](artifact/references/platforms/xiaohongshu.md)
- [Kuaishou API](artifact/references/platforms/kuaishou.md)
- [Weibo API](artifact/references/platforms/weibo.md)
- [Gongzhonghao API](artifact/references/platforms/gongzhonghao.md)
- [Baijiahao API](artifact/references/platforms/baijiahao.md)
- [Toutiaohao API](artifact/references/platforms/toutiaohao.md)
- [Qiehao API](artifact/references/platforms/qiehao.md)
- [Wangyihao API](artifact/references/platforms/wangyihao.md)
- [Shipinhao API](artifact/references/platforms/shipinhao.md)
- [Zhihu API](artifact/references/platforms/zhihu.md)
- [Dayuhao publishing parameters](artifact/references/platforms/dayuhao.md)
- [Souhuhao publishing parameters](artifact/references/platforms/souhuhao.md)
- [Jianshu publishing parameters](artifact/references/platforms/jianshu.md)
- [CSDN publishing parameters](artifact/references/platforms/csdn.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with HTTP examples, JSON payloads, and integration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include authenticated local API requests and platform-specific publish or analytics parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
