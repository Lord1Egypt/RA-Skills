## Description:

Web dashboard to approve OpenClaw device and channel pairings, manage connections, and access a live terminal from the browser.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dr1nnas](https://clawhub.ai/user/dr1nnas)

### License/Terms of Use:


## Use Case:

OpenClaw users and operators use this skill to review pending device and channel connections, approve or reject pairings, and administer a local OpenClaw environment through a browser-based dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard can expose sensitive OpenClaw pairing data, gateway tokens, and a host terminal.

Mitigation: Run only on a trusted local machine, keep the service bound to localhost, and do not expose the port beyond localhost without a hardened reverse proxy, TLS, and strong authentication.

Risk: Default dashboard and API credentials allow unauthorized access if left unchanged.

Mitigation: Change the dashboard username and password, set SERVER_AUTH_PASSWORD to a strong unique value, and set FLASK_SECRET_KEY to a random secret before first use.

Risk: The terminal feature provides shell access on the host machine.

Mitigation: Remove or disable the terminal route and template unless browser-based shell access is required and tightly controlled.

Risk: Changing passwords alone does not address the reported Socket.IO terminal/data exposure, token-in-page exposure, or XSS-prone rendering.

Mitigation: Rework the terminal Socket.IO authorization, avoid rendering gateway tokens into pages, sanitize untrusted pairing fields, and review the implementation before use with real OpenClaw credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dr1nnas/skills/approvals-ui)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline shell commands and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup and operating guidance for a local Flask and Socket.IO OpenClaw approvals dashboard.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
