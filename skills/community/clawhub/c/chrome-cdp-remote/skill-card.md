## Description:

Control Chrome/Chromium via CDP (Chrome DevTools Protocol) to open tabs, navigate URLs, take screenshots, and execute JavaScript on local or remote machines through an SSH tunnel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noestelar](https://clawhub.ai/user/noestelar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to automate Chrome or Chromium through Chrome DevTools Protocol commands without adding a full Playwright or Puppeteer dependency. It is useful for browser navigation, screenshots, JavaScript execution, local CDP sessions, and remote CDP sessions over SSH tunnels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CDP access grants broad control over the attached Chrome session and can affect logged-in accounts or sensitive browser data.

Mitigation: Use a dedicated disposable browser profile without personal sync, saved passwords, payment data, or important accounts.

Risk: Exposing a CDP port or SSH tunnel beyond localhost can allow unintended browser control.

Mitigation: Bind and tunnel CDP only to localhost, and stop Chrome and the SSH tunnel when the session is complete.

Risk: Python dependency installation can introduce package-management or supply-chain risk.

Mitigation: Install dependencies in a virtual environment and pin versions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noestelar/skills/chrome-cdp-remote)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline bash and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local and remote CDP setup guidance, verification commands, browser automation examples, and operational pitfalls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
