## Description: <br>
Control Chrome/Chromium via CDP (Chrome DevTools Protocol) to open tabs, navigate URLs, take screenshots, execute JavaScript, and work with local or SSH-tunneled remote browsers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[noestelar](https://clawhub.ai/user/noestelar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to launch or connect to Chrome with CDP enabled, automate browser actions, capture screenshots, execute JavaScript, and route remote browser control through an SSH tunnel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CDP access can control browser sessions, including logged-in accounts and sensitive pages. <br>
Mitigation: Use temporary or dedicated Chrome profiles, avoid attaching everyday or sensitive accounts unless intended, and remove saved browser state when finished. <br>
Risk: Exposed remote debugging ports can allow unintended browser control. <br>
Mitigation: Keep CDP bound to localhost, use SSH tunnels only with trusted hosts, and close tunnels when the task is complete. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/noestelar/chrome-cdp-remote) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides setup commands, connection patterns, and browser automation snippets for Chrome CDP.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
