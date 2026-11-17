## Description:

Browser MCP helps an agent control Chrome through the Chrome DevTools MCP protocol for website navigation, page inspection, element interaction, form filling, screenshots, and SSRF allowlist configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nasvip](https://clawhub.ai/user/nasvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to let an agent operate a Chrome profile for browsing, search, page review, screenshots, and multi-step web workflows in OpenClaw or QClaw. It is especially relevant when controlled browser access and explicit SSRF allowlist configuration are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent using this skill can see logged-in browser pages and act with that Chrome profile's account privileges.

Mitigation: Use a dedicated automation profile and require explicit confirmation before form submission, account changes, purchases, or other state-changing actions.

Risk: Exposing Chrome DevTools Protocol beyond localhost or allowing wildcard origins can make the browser controllable from unintended network paths.

Mitigation: Keep remote debugging bound to localhost, avoid wildcard origins, and do not expose the debugging port directly to a network.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nasvip/skills/browser-mcp)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with inline browser actions, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in browser navigation, screenshots, page snapshots, form interactions, and configuration changes when used by an agent with browser tooling.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
