## Description: <br>
Doubao Assistant Free is a Chinese-language Doubao API guide for conversation completion, web-search configuration, basic error handling, and multi-turn session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users use this skill to prepare Doubao chat-completion calls, decide when to enable web search, manage Chinese multi-turn conversations, and handle common API errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill declares write and exec permissions that are broader than its documented guide-style chat-helper purpose. <br>
Mitigation: Install only in a least-privileged or sandboxed agent environment, and narrow or justify write permission before treating the release as low risk. <br>
Risk: API examples can send prompts, files, or credentials to an external service once a real endpoint is configured. <br>
Mitigation: Use only approved Doubao/API endpoints, pass credentials through environment variables, and avoid sending sensitive data unless external processing is permitted. <br>
Risk: Web-search-assisted answers may be inaccurate, stale, or dependent on low-quality sources. <br>
Mitigation: Cross-check important, time-sensitive, legal, medical, financial, or operational answers against primary sources before acting on them. <br>
Risk: The artifact uses a placeholder API endpoint in examples. <br>
Mitigation: Replace the placeholder only with a verified endpoint and confirm the authentication, transport security, and data-handling policy before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/doubao-assistant-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes API request templates, environment-variable setup guidance, retry/error-handling notes, and JSON response examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
