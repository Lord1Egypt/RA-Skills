## Description:

免费、免第三方 API Key 的闲鱼竞品研究助手。用户想在闲鱼搜索同类商品、比较公开可见的价格、成色、图片、卖点和交易条件，或为选品和文案找证据时使用。它通过用户已登录的 Easy WebBridge 浏览器读取页面，只记录看得到的内容，不自动购买、联系、收藏或发布。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

闲鱼卖家和选品人员可用此技能在已登录的浏览器中检索公开商品，整理可见价格、成色、规格、卖点和交易方式，并生成带来源链接的竞品样本报告。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan 将此版本评为可疑（中等置信度），提示表格导出存在公式注入风险。

Mitigation: 打开导出文件前检查单元格内容，并将采集到的文本视为不可信输入。

Risk: 安全评估指出桥接凭据处理未充分说明，且部分可执行内容仅经过部分检查。

Mitigation: 使用前审阅相关文件并确认 Easy WebBridge 的凭据处理方式；不要向技能提供或保存 Cookie、密码或 Token。

## Reference(s):

- [闲鱼竞品采集字段说明](references/采集字段.md)
- [Easy WebBridge 安装与源码说明](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge Gitee 镜像](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR 官方客户端下载页](https://www.ebrower.com/down.html)

## Skill Output:

**Output Type(s):** [Analysis, Files, JSON, CSV, Markdown]

**Output Format:** [JSON、CSV 和 Markdown 竞品采样报告]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [保留商品来源链接；缺失字段留空；分析范围限于本次页面可见样本。]

## Skill Version(s):

1.1.1 (source: package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
