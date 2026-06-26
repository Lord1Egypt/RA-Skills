## Description: <br>
Android GUI automation via MCP: MiniMax or another MCP client calls uiautomator2 tools to control Android phone screens for app control, price monitoring, social posting, screen scraping, screenshots, clicks, swipes, text entry, scheduling, and alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to connect an AI agent to Android devices through Termux, MCP, and uiautomator2 so the agent can operate mobile apps, collect UI evidence, compare prices, schedule checks, and send alerts. It is intended for controlled Android automation workflows where the operator is prepared to scope and review device actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent can exercise broad live control over an Android device and logged-in apps. <br>
Mitigation: Use a dedicated phone or test accounts, keep sensitive apps such as banking, messaging, and authenticators out of scope, and gate any high-impact action before execution. <br>
Risk: Screenshots, UI dumps, clipboard access, and file transfer can expose private or account-specific data. <br>
Mitigation: Disable or manually approve screenshots, UI dumps, clipboard access, push and pull file operations, and shell access unless they are required for the current task. <br>
Risk: The skill includes flows for posting content and sending outbound Telegram alerts. <br>
Mitigation: Require human review for every public post or outbound notification before it is sent. <br>
Risk: App clear, app install, shell, and remote ADB operations can modify device state or installed software. <br>
Mitigation: Run only in a scoped Termux or ADB environment and manually gate shell, app install, app clear, and remote connection operations. <br>


## Reference(s): <br>
- [Android GUI Automation setup guide](references/setup-guide.md) <br>
- [uiautomator2-mcp package](https://pypi.org/project/uiautomator2-mcp/) <br>
- [uiautomator2 project](https://github.com/openatx/uiautomator2) <br>
- [ClawHub release page](https://clawhub.ai/smseow001/android-gui-automation) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, MCP tool calls] <br>
**Output Format:** [Markdown with bash, JSON, and Python snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup steps and examples for Android device control, screenshots, UI extraction, app automation, scheduled monitoring, and outbound alerts.] <br>

## Skill Version(s): <br>
3.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
