## Description: <br>
Automates a real Chrome browser through Chrome Debug Protocol to navigate, click, fill forms, extract page data, take screenshots, and run multi-step browser workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScottLiu007](https://clawhub.ai/user/ScottLiu007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to direct an agent through real browser tasks such as navigation, form filling, data extraction, screenshots, and multi-step web workflows while preserving the user's Chrome session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control of a real Chrome browser session, which can expose logged-in accounts or sensitive page data. <br>
Mitigation: Use a dedicated automation-only Chrome profile and avoid sensitive logged-in accounts when running browser automation. <br>
Risk: Chrome Debug Protocol control can be started or used without enough user consent for account-changing actions. <br>
Mitigation: Require explicit user consent before starting CDP control, entering credentials, submitting forms, sending messages, deleting content, making purchases, or changing account state. <br>
Risk: Using an unpinned Playwright MCP package can change automation behavior between runs. <br>
Mitigation: Pin and review the MCP package version before installation, and stop the debug Chrome process when automation is finished. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ScottLiu007/auto-browser) <br>
- [Publisher profile](https://clawhub.ai/user/ScottLiu007) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Chrome debug endpoint and a Playwright CDP MCP tool configured for the user's browser session.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
