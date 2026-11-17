## Description:

Attaches an agent to the user's own already-logged-in Chromium browser over CDP with Playwright so tasks can reuse an existing session while the user watches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill when an automation task must run in their own already-authenticated browser session, such as working in a dashboard protected by SSO or 2FA. It is not intended for ordinary public browsing, scraping, or headless testing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can control a browser session that is already logged in to the user's accounts.

Mitigation: Use only with the user's present consent, keep the user watching, and confirm high-impact actions before submission.

Risk: An open CDP debug port or SSH tunnel can expose live browser control to other local or forwarded processes.

Mitigation: Bind CDP and tunnels to loopback, avoid public forwarding, close the tunnel after use, and restart the browser normally to remove the debug port.

Risk: One-time secrets may be written to plaintext files during capture workflows.

Mitigation: Avoid the secret-to-file workflow when possible; if used, move secrets directly into the user's password manager and delete the temporary file immediately.

## Reference(s):

- [Launch and drive](references/launch-and-drive.md)
- [Remote agent and local browser tunnel](references/remote-over-tunnel.md)
- [Selectors, handoffs, secrets, cleanup](references/selectors-and-handoffs.md)
- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/browser-driver)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash and JavaScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce step screenshots and temporary files during browser-control workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
