## Description:

使用用户指定的 Easy WebBridge 浏览器环境和UP主主页，读取最多10条当前可见视频，交付含标题、日期、主题、链接、来源与缺项的近期更新摘要草稿；适合一次性核对公开更新。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

希望核对公开投稿的用户可使用此技能，从指定的 B 站 UP 主主页整理最多 10 条当前可见视频。它输出带有标题、页面显示日期、主题、视频链接、来源和缺项说明的更新摘要。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 安全评估指出，安装命令未固定版本，摘要所述用途与报告的安装行为存在不一致，且部分文件未能完整检查。

Mitigation: 安装前检查包内容和浏览器操作；选用已审阅的版本，若实际行为偏离摘要任务或页面要求登录或安全验证，则停止。

## Reference(s):

- [Easy WebBridge](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Bilibili adapter documentation](https://github.com/xxjrq/easy-webbridge/blob/main/docs/adapters/browser/bilibili.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown table with source links and omissions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [最多整理10条当前可见视频；未显示的日期保持空白，不推断无法看到的信息。]

## Skill Version(s):

1.0.2 (source: server-resolved release and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
