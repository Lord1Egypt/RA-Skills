## Description: <br>
Unified CLI gateway to search, install, authenticate, and invoke enterprise and AI platform tools including WeCom, DingTalk, Lark/Feishu, and Dreamina for messaging, calendars, documents, meetings, and AI media generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxyd-ai](https://clawhub.ai/user/lxyd-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when they need an agent to find the right CLI operation, inspect its parameters, and run provider tools for enterprise workflows or AI image and video creation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install tools, authenticate to work accounts, and perform account-changing actions across connected providers. <br>
Mitigation: Use isolated installation methods such as pipx or uv, authenticate only the needed provider, and require the agent to show the exact command before sending messages, changing business data, or spending generation credits. <br>
Risk: Provider operations can fail or target the wrong action if the agent guesses command IDs or parameters. <br>
Mitigation: Require the documented search and info workflow before each run so the agent confirms the tool ID, schema, and example invocation. <br>
Risk: Dreamina generation can consume paid credits and returns asynchronous job results. <br>
Mitigation: Warn the user before generation, run one task at a time, and query the submitted job result before continuing. <br>


## Reference(s): <br>
- [agent-cli-hub PyPI project](https://pypi.org/project/agent-cli-hub/) <br>
- [cli-hub source repository](https://github.com/agentrix-ai/clihub) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON argument examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce provider-specific command invocations, authentication steps, and generated media job follow-up guidance.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
