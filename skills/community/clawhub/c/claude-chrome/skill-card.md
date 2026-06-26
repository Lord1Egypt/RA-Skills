## Description: <br>
Use Claude Code with Chrome browser extension for web browsing and automation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dgriffin831](https://clawhub.ai/user/dgriffin831) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to route browsing, page interaction, form filling, and web automation tasks through Claude Code's Chrome extension when a Chrome desktop session is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad auto-approval can allow Claude Code to take unintended browser actions during noninteractive automation. <br>
Mitigation: Use a dedicated Chrome profile or test account, avoid sensitive logged-in sessions, and keep browser prompts narrow and low-impact. <br>
Risk: Browser automation tasks may continue in the background after gateway or command timeouts. <br>
Mitigation: Use explicit command timeouts, monitor running `claude` processes, and stop background processes when a task is no longer needed. <br>
Risk: New domain permission prompts from the Chrome extension can block unattended runs. <br>
Mitigation: Confirm the extension is active and approve required domains before relying on unattended browser automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dgriffin831/claude-chrome) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
