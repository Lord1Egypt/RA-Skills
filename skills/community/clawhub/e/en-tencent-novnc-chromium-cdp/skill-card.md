## Description:

One-click deployment of a shared visual browser using Linux noVNC, Chromium, and CDP or Windows Edge/Chrome CDP for agent-controlled web automation with manual login and verification handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangleizhui](https://clawhub.ai/user/kangleizhui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy or take over a visible browser that both the user and agent can inspect and control. It is intended for web workflows that need automation plus manual handling of logins, QR codes, CAPTCHAs, or similar verification steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests broad root or sudo access and may ask for SSH access during deployment.

Mitigation: Run it only on an isolated or disposable server when possible, avoid sharing SSH passwords in chat, and remove temporary sudoers entries after deployment.

Risk: The skill opens remote browser access and can install persistent remote-control services.

Mitigation: Do not expose noVNC or CDP broadly; restrict network access, keep CDP on localhost unless explicitly needed, and remove persistent services when the browser is no longer required.

Risk: The security verdict is suspicious because the skill combines a plausible remote-browser purpose with unsafe deployment defaults.

Mitigation: Review the skill carefully before installing, scan the host configuration after use, and prefer disposable infrastructure for high-risk browsing workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kangleizhui/skills/en-tencent-novnc-chromium-cdp)
- [Publisher profile](https://clawhub.ai/user/kangleizhui)
- [noVNC repository](https://github.com/novnc/noVNC.git)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment reminders, browser control steps, service configuration guidance, and completion details such as noVNC and CDP endpoints.]

## Skill Version(s):

1.0.45 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
