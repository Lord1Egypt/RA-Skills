## Description: <br>
One-click deploy remote visual browser for Linux noVNC plus Chromium CDP on headless servers, and Windows Edge or Chrome CDP takeover, so an AI agent and user can share a browser for login, CAPTCHA, QR-code, and web automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kangleizhui](https://clawhub.ai/user/kangleizhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deploy or attach to a visible browser that an AI agent can control through CDP while a person can manually handle logins, CAPTCHAs, QR codes, and other verification steps. It is intended for browser automation, content publishing, backend management, and troubleshooting workflows that require shared human-agent visibility. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill needs root or sudo-level access to install system packages, write service files, and create persistent remote-browser services. <br>
Mitigation: Run setup yourself where possible, use temporary least-privilege access, review commands before execution, and remove elevated access after deployment. <br>
Risk: The fallback flow asks for SSH passwords in chat, which can expose reusable credentials. <br>
Mitigation: Do not paste reusable SSH passwords into chat; prefer passwordless sudo setup performed locally, temporary credentials, SSH keys, or another controlled access method. <br>
Risk: noVNC on port 6080 creates a remote browser access surface. <br>
Mitigation: Restrict port 6080 with a firewall, cloud security group, VPN, or source-IP allowlist, and disable the services when the browser is no longer needed. <br>
Risk: Exposing the CDP debug port could allow browser takeover. <br>
Mitigation: Keep CDP bound to localhost and do not expose port 9223 publicly unless remote debugging is explicitly required and tightly source-restricted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kangleizhui/skills/en-tencent-novnc-chromium-cdp) <br>
- [Publisher Profile](https://clawhub.ai/user/kangleizhui) <br>
- [noVNC Project](https://github.com/novnc/noVNC.git) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, PowerShell, Python, URLs, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce deployment status, noVNC access details, CDP endpoint checks, screenshots, and remediation guidance.] <br>

## Skill Version(s): <br>
1.0.45 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
