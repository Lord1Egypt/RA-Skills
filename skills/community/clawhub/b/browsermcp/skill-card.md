## Description: <br>
Automate browser tasks using the BrowserMCP MCP server and Chrome extension for navigation, form filling, clicks, screenshots, and console log retrieval in the user's existing browser profile. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankausberlin](https://clawhub.ai/user/frankausberlin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to automate real-browser workflows that need an active Chrome tab, existing authenticated sessions, page inspection, interaction, and visual or console verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate actions in a connected logged-in Chrome tab. <br>
Mitigation: Use a separate Chrome profile with only the needed accounts, connect only the intended tab, and require explicit confirmation before submitting forms, posting, purchasing, changing account data, or accepting terms. <br>
Risk: The setup uses an unpinned external runtime package. <br>
Mitigation: Review or pin the BrowserMCP package version instead of using `@latest` when deploying in controlled environments. <br>
Risk: Sensitive pages may expose banking, administrative, or personally identifiable information to the automation workflow. <br>
Mitigation: Avoid banking, administrative, and PII-heavy pages unless the task clearly requires them and the user has approved the action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankausberlin/browsermcp) <br>
- [BrowserMCP setup guide](references/setup.md) <br>
- [BrowserMCP tools reference](references/tools.md) <br>
- [BrowserMCP workflows](references/workflows.md) <br>
- [BrowserMCP best practices](references/best-practices.md) <br>
- [BrowserMCP website](https://browsermcp.io) <br>
- [BrowserMCP documentation](https://docs.browsermcp.io) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration, and tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a running BrowserMCP server, installed Chrome extension, and an explicitly connected active browser tab.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
