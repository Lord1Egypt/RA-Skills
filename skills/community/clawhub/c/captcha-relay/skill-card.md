## Description:

Human-in-the-loop CAPTCHA solving with two modes: screenshot (default, zero infrastructure) and token relay (requires network access).

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xclanky](https://clawhub.ai/user/0xclanky)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation operators use this skill to route CAPTCHA challenges to a human solver, either by sharing an annotated screenshot for manual clicks or by serving a native CAPTCHA widget and injecting the returned token into a controlled browser session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay mode can expose CAPTCHA-solving workflows and browser interaction over a reachable network endpoint without enough access controls.

Mitigation: Prefer screenshot mode, localhost, or a tightly controlled private network such as Tailscale; avoid public tunnels and require per-session secrets before exposing the relay.

Risk: The skill can interact with an active Chrome session through CDP and inject clicks or CAPTCHA tokens into the page.

Mitigation: Use only on authorized sites and controlled browser sessions, isolate the browser profile, and close the relay and CDP-enabled browser after use.

Risk: Solved CAPTCHA tokens are written to a predictable temporary file for external consumers.

Mitigation: Run on trusted hosts, restrict local user access, and remove temporary token files after each solving session.

Risk: Tunnel startup may use an unpinned npx localtunnel path or optional external tunnel tooling.

Mitigation: Pin and review tunnel tooling and dependency versions before production use, or disable public tunneling and use private connectivity.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/0xclanky/skills/captcha-relay)
- [README](README.md)
- [Architecture](ARCHITECTURE.md)
- [Tailscale Setup](TAILSCALE.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands plus JSON CLI events, relay URLs, screenshot paths, and CAPTCHA tokens from the runtime helper.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+, Chrome or Chromium with CDP enabled on the configured port, and optional private network or tunnel access for relay mode.]

## Skill Version(s):

2.1.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
