## Description: <br>
Controls a local logged-in Chrome browser through Chrome DevTools MCP for browsing, page interaction, screenshots, DOM access, and JavaScript execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lumint](https://clawhub.ai/user/lumint) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a real Chrome session for web browsing, logged-in site interaction, X/Twitter workflows, page structure extraction, screenshots, and JavaScript execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate a real logged-in Chrome session and perform account-changing actions. <br>
Mitigation: Use a separate Chrome profile with only the accounts needed and require explicit confirmation before posting, deleting, purchases, form submissions, account changes, messages, or JavaScript execution. <br>
Risk: Chrome remote debugging enables direct browser control while it is active. <br>
Mitigation: Keep remote debugging disabled when not actively using the skill. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/lumint/chrome-mcp) <br>
- [X home](https://x.com/home) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with Chrome DevTools MCP tool names, CSS selectors, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can direct browser navigation, DOM interaction, screenshots, and JavaScript execution in a logged-in Chrome session.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
