## Description: <br>
实时采集抖音直播弹幕，使用 DeepSeek AI 分析观众意图，并按主播人设生成个性化回复建议。 <br>

This skill is for research and development only. <br>

## Publisher: <br>
[go522000](https://clawhub.ai/user/go522000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Live-stream operators and developers use this skill to monitor Douyin live-chat messages, filter low-value messages, and draft short AI-assisted replies for e-commerce, education, gaming, entertainment, or knowledge-sharing streams. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a large obfuscated Douyin signing script under Node. <br>
Mitigation: Review or sandbox sign.js before use, and run the skill in an isolated environment. <br>
Risk: The WebSocket client disables certificate verification. <br>
Mitigation: Restore certificate verification or restrict execution to a trusted network and monitored environment. <br>
Risk: Viewer chat data is stored locally and sent to the DeepSeek API for reply generation. <br>
Mitigation: Treat chat logs and reply caches as viewer data; obtain appropriate consent, protect stored files, and delete data on a defined schedule. <br>
Risk: DeepSeek API credentials can be configured in code. <br>
Mitigation: Provide the API key through an environment variable and avoid committing or sharing configured credentials. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/go522000/douyin-live-ai) <br>
- [AI prompt references](references/prompts.md) <br>
- [DeepSeek API platform](https://platform.deepseek.com) <br>
- [WorkBuddy skill platform](https://www.codebuddy.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces concise setup and operation guidance for a live-chat assistant that logs viewer messages, generated replies, and cache entries locally.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
