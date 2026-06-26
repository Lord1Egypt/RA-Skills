## Description: <br>
Control the user's local Chrome browser through the OpenClaw Browser Relay extension for tab access, browser automation, screenshots, page reading, and interactions in existing logged-in sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meowlegemy-sudo](https://clawhub.ai/user/meowlegemy-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they intentionally want an agent to control selected local Chrome tabs, including reading page content, navigating, clicking, typing, and taking screenshots in existing browser sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can act inside selected Chrome tabs, including sites where the user is already signed in. <br>
Mitigation: Install and use it only when browser control is intentional; keep the extension detached except when needed and attach only the intended tab. <br>
Risk: The gateway token grants relay access and could be misused if exposed. <br>
Mitigation: Treat the gateway token as a secret and verify token settings if the extension reports a mismatch. <br>
Risk: Browser automation on sensitive sites can perform unintended actions in authenticated sessions. <br>
Mitigation: Avoid sensitive sites unless necessary and review planned actions before allowing automation. <br>


## Reference(s): <br>
- [Chrome Relay on ClawHub](https://clawhub.ai/meowlegemy-sudo/chrome-relay) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown with inline shell commands and browser tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the Chrome Browser Relay extension, a gateway token, and an attached Chrome tab.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
