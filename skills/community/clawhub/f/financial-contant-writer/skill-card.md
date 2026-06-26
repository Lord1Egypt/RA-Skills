## Description: <br>
财税审计内容生成器 - 快速生成专业财税公众号文章，支持多种文章类型和主题 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fengbabao0929](https://clawhub.ai/user/fengbabao0929) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators, finance professionals, and tax or audit content teams use this skill to draft Chinese WeChat public account articles, outlines, title options, review notes, and related image selections for finance, tax, audit, policy, and risk topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release bundles valuation and investment-advice workflows that may be regulated or unsuitable for general content automation. <br>
Mitigation: Disable or exclude the valuation guides unless the deployment has qualified financial review, suitability controls, and clear user-facing disclaimers. <br>
Risk: The command manifest uses absolute Windows paths that are unlikely to work unchanged in other environments. <br>
Mitigation: Replace hard-coded paths with deployment-local paths before enabling slash commands. <br>
Risk: The image generator includes an exposed Unsplash API key. <br>
Mitigation: Remove the bundled key, rotate it if it was live, and inject image API credentials through a managed secret or environment variable. <br>
Risk: Coze, WeChat, database, search, and document-conversion integrations can expose sensitive finance, tax, or client data. <br>
Mitigation: Connect external services only after privacy review, data minimization, access controls, and approval for the specific data classes being processed. <br>
Risk: Generated tax, audit, finance, and policy content may be outdated, incomplete, or misleading. <br>
Mitigation: Require professional review against current authoritative sources before publication or client use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fengbabao0929/financial-contant-writer) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Command manifest](artifact/finance-content-skill.json) <br>
- [WeChat Finance Writer Coze Guide](artifact/wechat-finance-writer-coze.md) <br>
- [Coze Complete Configuration Guide v4](artifact/finance-writer-coze-quickstart-v4.md) <br>
- [Finance Valuation Agent Guide](artifact/finance-valuation-agent-guide.md) <br>
- [Finance Valuation Coze Guide](artifact/finance-valuation-coze-guide.md) <br>
- [Coze](https://www.coze.cn/) <br>
- [ConvertAPI Markdown to Word endpoint](https://api.convertapi.com/Word/MdToWord) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and plain text, with optional JSON command configuration and saved file metadata.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language finance, tax, audit, policy, and risk content intended for WeChat public account workflows; generated professional content should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
