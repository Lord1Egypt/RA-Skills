## Description:

免费下载抖音视频、图文图片和作品音轨，不用注册第三方下载站，也不需要 TikHub、redfox 等第三方 API Key。用户要求下载抖音作品、图文图片或音轨时使用；支持抖音作品长链、数字 ID，以及可由单次安全 HTTPS 响应解析的分享短链。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT No Attribution

## Use Case:

面向需要保存抖音作品的用户和创作者。用户提供作品链接或 ID 后，技能通过所选浏览器下载视频、图文图片或音轨，并报告保存位置。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: 浏览器配置文件授权说明不一致，可能导致代理在没有清楚授权时选择或新建配置文件。

Mitigation: 指定确切的 browserId；对新建、切换、启动浏览器配置文件或安装软件分别取得用户许可。优先使用经过审查的安装包版本和代码仓库修订。

## Reference(s):

- [EasyBR AI 操作指南](https://www.ebrower.com/helperdoc/ai-agent-workflow.html)
- [Easy WebBridge 指南](https://www.ebrower.com/helperdoc/easy-webbridge.html)
- [Easy WebBridge 项目](https://github.com/xxjrq/easy-webbridge)

## Skill Output:

**Output Type(s):** [Files, Media]

**Output Format:** [本地视频、图片或 48 kHz 双声道 MP3 文件，并附保存路径和基础媒体信息]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [按作品标题命名；图文作品可生成多张图片文件。]

## Skill Version(s):

1.1.6 (source: package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
