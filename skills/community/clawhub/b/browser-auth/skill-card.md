## Description: <br>
Start a secure remote browser tunnel for manual user authentication (solving Captchas, 2FA, logins) and capture session data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lksrz](https://clawhub.ai/user/lksrz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill when a website requires manual login, Captcha solving, or 2FA before an agent can continue authenticated browser work. It captures reusable browser session data after the user completes authentication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles reusable login sessions that can grant account access if exposed. <br>
Mitigation: Keep the tokenized link private, run the browser in an isolated environment for sensitive accounts, and delete the generated session file immediately after use. <br>
Risk: The browser-control server may be exposed more broadly than intended when AUTH_HOST is not constrained. <br>
Mitigation: Set AUTH_HOST=127.0.0.1 unless using a trusted tunnel, and avoid direct public binding for authentication sessions. <br>


## Reference(s): <br>
- [ClawHub Browser Auth release](https://clawhub.ai/lksrz/browser-auth) <br>
- [AI Commander homepage](https://aicommander.dev) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Guidance] <br>
**Output Format:** [Session JSON file plus terminal status output and Markdown usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, chromium-browser, express, socket.io, and playwright-core; may use AUTH_HOST, AUTH_TOKEN, and BROWSER_PROXY environment variables.] <br>

## Skill Version(s): <br>
1.6.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
