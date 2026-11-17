## Description:

Set up a remote-controlled Chrome browser on an Ubuntu/Debian VPS with noVNC visual access over SSH and optional authenticated HTTP proxy routing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[osipov-anton](https://clawhub.ai/user/osipov-anton)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure a remotely controllable Chrome browser on a Linux VPS for agent automation, live noVNC viewing, and optional proxy-routed browsing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup combines root-level VPS changes, disabled Chrome sandboxing, and remote browser control services.

Mitigation: Use an isolated rebuildable VPS, remove Chrome --no-sandbox/noSandbox=true where possible, run the stack as an unprivileged user, and bind noVNC, websockify, and CDP to loopback.

Risk: Proxy credentials and broad firewall changes can expose sensitive access or weaken host network controls.

Mitigation: Avoid inline proxy credentials and review firewall rules manually instead of applying the provided UFW block unchanged.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/osipov-anton/skills/browser-vps-setup-skill)
- [Google Chrome Linux package](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb)
- [IP address verification endpoint](https://api.ipify.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash, JSON, and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target Ubuntu/Debian VPS environments and require manual security review before execution.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact metadata version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
