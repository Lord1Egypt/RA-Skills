## Description: <br>
Automatically consults official documentation first to resolve configuration, usage, permission, or error issues with tools and APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ekin-chn](https://clawhub.ai/user/ekin-chn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when technical answers depend on current official documentation, such as API usage, CLI options, permissions, authentication, environment variables, and error handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Frequent documentation lookups can add latency or surface documentation for the wrong product version. <br>
Mitigation: Confirm the relevant product or API version before relying on a result, and cite the documentation version, URL, or access date in user-facing answers. <br>
Risk: Configuration guidance can affect authentication, permissions, or environment variables. <br>
Mitigation: Review proposed configuration changes before applying them, especially when credentials, access scopes, or environment variables are involved. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ekin-chn/doc-first) <br>
- [OpenClaw documentation](https://docs.openclaw.ai/llms.txt) <br>
- [OpenAI documentation](https://platform.openai.com/docs) <br>
- [Anthropic documentation](https://docs.anthropic.com/) <br>
- [GLM API documentation](https://open.bigmodel.cn/dev/api) <br>
- [MiniMax documentation](https://www.minimaxi.com/document/Guide) <br>
- [DashScope documentation](https://qianwen-api.aliyun.com/) <br>
- [Qianfan documentation](https://qianfan.cloud.baidu.com/) <br>
- [iFlyTek Spark documentation](https://www.xfyun.cn/doc/spark/) <br>
- [Moonshot platform documentation](https://platform.moonshot.cn/) <br>
- [Tiangong documentation](https://www.tiangong.cn/) <br>
- [Coze documentation](https://www.coze.cn/docs/) <br>
- [WeChat Mini Program documentation](https://developers.weixin.qq.com/miniprogram/dev/framework/) <br>
- [Telegram Bot API](https://core.telegram.org/bots/api) <br>
- [DeepSeek documentation](https://api.deepseek.com/docs) <br>
- [Slack API documentation](https://api.slack.com/) <br>
- [Discord developer documentation](https://discord.com/developers/docs) <br>
- [GitHub REST API documentation](https://docs.github.com/rest) <br>
- [Notion API documentation](https://developers.notion.com/docs/getting-started) <br>
- [Gmail API documentation](https://developers.google.com/gmail/api) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with cited documentation references and inline commands or configuration snippets when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emphasizes official documentation, version awareness, and uncertainty disclosure.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
