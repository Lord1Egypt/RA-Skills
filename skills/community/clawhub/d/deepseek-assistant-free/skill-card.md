## Description: <br>
Deepseek Assistant Free provides Chinese-language guidance for using the DeepSeek API for general chat, code generation, basic reasoning, request templates, error handling, and token-cost estimation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to choose DeepSeek models and draft API request patterns for chat, coding assistance, and basic reasoning workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may send selected prompts or code to the DeepSeek API. <br>
Mitigation: Use it only with content you have explicitly chosen to share with DeepSeek, and avoid secrets, private files, regulated data, or broad project context. <br>
Risk: The artifact requests write and exec capabilities even though the security summary identifies unnecessary write permission. <br>
Mitigation: Grant the minimum permissions needed for a specific task and review generated commands before execution. <br>
Risk: Callback and export language is ambiguous about data handling boundaries. <br>
Mitigation: Do not provide callback URLs or export destinations until the receiving endpoint and transmitted data are reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/deepseek-assistant-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [DeepSeek chat completions API endpoint](https://api.deepseek.com/v1/chat/completions) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JavaScript examples, tables, and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include DeepSeek API request templates, environment-variable setup, model selection notes, error-handling guidance, and token-cost estimates.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
