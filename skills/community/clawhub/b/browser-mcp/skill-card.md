## Description: <br>
Automates Chrome browser navigation, search, page inspection, screenshots, and element interactions through Chrome DevTools MCP for OpenClaw/QClaw workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nasvip](https://clawhub.ai/user/nasvip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent drive a Chrome browser for website navigation, search, form interaction, screenshots, and multi-step page workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate an already logged-in Chrome session. <br>
Mitigation: Use a dedicated low-privilege Chrome profile and require explicit confirmation before submitting forms, posting content, changing account settings, or using authenticated sites. <br>
Risk: Chrome DevTools remote debugging can expose browser control if port 9222 is reachable from a network. <br>
Mitigation: Keep DevTools bound to localhost and do not expose port 9222 on a network. <br>
Risk: Overly broad SSRF allowlists can allow unintended browsing targets. <br>
Mitigation: Keep SSRF allowlists narrow and review allowed domains before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nasvip/browser-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill guides browser actions and configuration rather than producing standalone application files.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
