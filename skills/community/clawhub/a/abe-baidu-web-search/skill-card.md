## Description: <br>
Baidu Web Search lets agents retrieve real-time web search results through SkillBoss API Hub for fact-checking, news, and other up-to-date information requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill when a response needs current web information, source-backed fact checking, latest news, or verification of people, products, places, and events. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user search queries to SkillBoss for web retrieval. <br>
Mitigation: Do not use it for confidential, personal, internal, or credential-containing queries. <br>
Risk: The skill requires a SkillBoss API key. <br>
Mitigation: Configure the key through the platform or a private local config and avoid exposing it in public chats, screenshots, recordings, or logs. <br>
Risk: Broad auto-use wording may trigger searches more often than expected. <br>
Mitigation: Confirm search intent before using the skill for sensitive or ambiguous requests. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/abeltennyson/abe-baidu-web-search) <br>
- [Publisher profile](https://clawhub.ai/user/abeltennyson) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON search results for the agent, with Markdown-facing guidance and shell command examples in the skill instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include title, URL, snippet, total, and query fields; result count defaults to 20 and is capped at 50.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
