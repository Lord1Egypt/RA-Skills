## Description: <br>
Browser Driver guides an agent to attach to a user's own logged-in Chromium browser over CDP with Playwright so it can perform supervised browser actions in an existing session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when a task needs their existing authenticated browser session, such as supervised dashboard changes behind SSO or 2FA, and a fresh browser would force a new login. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill controls an already-signed-in browser through CDP, which can affect the user's active accounts if used outside the intended scope. <br>
Mitigation: Use it only with the user's present consent, keep the user watching the session, screenshot after mutating actions, and hand identity checks back to the user. <br>
Risk: An exposed CDP port can allow another process or host to control the logged-in browser. <br>
Mitigation: Keep CDP bound to localhost, use loopback-only SSH tunnels when remote access is needed, close tunnels when finished, and restart the browser normally afterward. <br>
Risk: One-time secrets shown in the browser could be leaked through chat, logs, or leftover temporary files. <br>
Mitigation: Capture secrets directly to a temporary local file only when necessary, move them into the user's password manager, avoid pasting them into chat, and remove the temporary file afterward. <br>


## Reference(s): <br>
- [Browser Driver on ClawHub](https://clawhub.ai/clarezoe/browser-driver) <br>
- [Launch and Drive](references/launch-and-drive.md) <br>
- [Remote Over Tunnel](references/remote-over-tunnel.md) <br>
- [Selectors and Handoffs](references/selectors-and-handoffs.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript Playwright snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce supervised browser-driving steps, temporary screenshots, and temporary secret files when the user chooses that workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
