## Description: <br>
Human-in-the-loop CAPTCHA solving with two modes: screenshot mode captures the page with a grid overlay and injects clicks based on a human reply, while token relay mode detects CAPTCHA type and sitekey, serves the real widget on a relay page for native solving, and injects the token via CDP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xclanky](https://clawhub.ai/user/0xclanky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation operators use this skill to route CAPTCHA challenges to a human solver through screenshot-based click selection or a relay page, then continue the browser workflow through CDP injection. It is intended for authorized workflows the user controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay URLs and screenshots can expose browser or session data. <br>
Mitigation: Treat them as sensitive, avoid sensitive logged-in pages, and share them only with the intended human solver. <br>
Risk: Network-facing relay modes may expose browser/session control through unauthenticated relays. <br>
Mitigation: Prefer private Tailscale or LAN access over public tunnels and stop relay services after use. <br>
Risk: CAPTCHA relay and token injection can be misused on third-party services. <br>
Mitigation: Use only for authorized testing or workflows you control and do not use token-injection features without explicit permission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xclanky/captcha-relay) <br>
- [README](artifact/README.md) <br>
- [Architecture](artifact/ARCHITECTURE.md) <br>
- [Tailscale setup](artifact/TAILSCALE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with inline JavaScript and shell examples; CLI/module calls return JSON-like result objects and screenshot file paths.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce relay URLs, CAPTCHA tokens, annotated screenshot files, and CDP browser actions.] <br>

## Skill Version(s): <br>
2.1.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
