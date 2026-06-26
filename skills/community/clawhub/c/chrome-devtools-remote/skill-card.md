## Description: <br>
Drive a remote chrome-devtools-mcp server over HTTPS with the chrome-devtools CLI to navigate, screenshot, inspect, or evaluate JavaScript in a browser running on another host. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dzianisv](https://clawhub.ai/user/dzianisv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to control a remote Chrome browser when they need to inspect web apps, capture screenshots, run JavaScript, or debug pages on another host without local Chrome access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote browser automation can expose authenticated pages, form inputs, screenshots, cookies, and stored browser state to a remote service. <br>
Mitigation: Install only when the remote browser operator is trusted; prefer least-privilege test accounts or disposable sessions and avoid highly sensitive logins. <br>
Risk: Server-side browser sessions can preserve tab state between commands. <br>
Mitigation: End remote sessions when work is complete and use clear procedures for deleting stored sessions and browser state. <br>
Risk: Using insecure remote connections can weaken transport protection. <br>
Mitigation: Use insecure TLS options only for expected self-signed tailnet endpoints; prefer endpoints with valid certificates and verify the remote URL before sending data. <br>


## Reference(s): <br>
- [Chrome Devtools Remote on ClawHub](https://clawhub.ai/dzianisv/chrome-devtools-remote) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local screenshot paths and structured JSON returned by the chrome-devtools CLI.] <br>

## Skill Version(s): <br>
0.26.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
