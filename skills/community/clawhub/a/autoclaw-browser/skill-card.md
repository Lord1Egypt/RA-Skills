## Description: <br>
AutoClaw Browser Automation lets an agent control Chrome through an MCP server and companion extension for navigation, screenshots, bookmarks, forms, page inspection, cookies, storage, and workflow playback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addogiavara-tech](https://clawhub.ai/user/addogiavara-tech) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill to let an agent operate browser tabs, extract page data, manage bookmarks, capture screenshots, and run repeatable browser workflows. It is intended for users who intentionally want agent-driven control over local or authenticated browsing sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent persistent control over authenticated browser tabs. <br>
Mitigation: Use it only when full browser control is intended, avoid sensitive tabs, disable auto-attach-all unless needed, and stop the MCP server when work is complete. <br>
Risk: Weak or shared authentication can expose browser control to unintended local clients. <br>
Mitigation: Set a unique token instead of relying on the built-in token, and keep the server bound to local use only while needed. <br>
Risk: Cookies, storage, screenshots, JavaScript execution, bookmark deletion, login-session restore, cloud API keys, and bridge calls are high-risk browser operations. <br>
Mitigation: Review requested tool calls before execution and restrict use to tabs and accounts where these operations are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addogiavara-tech/autoclaw-browser) <br>
- [Publisher profile](https://clawhub.ai/user/addogiavara-tech) <br>
- [AutoClaw website](https://www.wboke.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL](artifact/SKILL.md) <br>
- [Artifact changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [MCP tool responses as text or JSON, plus setup guidance in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Tool results can include page content, screenshots, bookmark data, cookies, storage values, action logs, and browser automation status.] <br>

## Skill Version(s): <br>
6.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
