## Description:

Automate Electron desktop apps (VS Code, Slack, Discord, Figma, Notion, Spotify, etc.) using agent-browser via Chrome DevTools Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daxiangnaoyang](https://clawhub.ai/user/daxiangnaoyang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to connect an agent to running Electron desktop applications, inspect app state, interact with UI elements, take screenshots, extract data, and automate testing or operational workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can let an agent inspect and control authenticated Electron desktop apps through debugging ports.

Mitigation: Use only on trusted machines, prefer isolated test profiles, and avoid highly sensitive apps.

Risk: Open debugging ports can expose desktop app control if they are reachable beyond the intended local session.

Mitigation: Verify debugging ports are local-only and close the apps or ports after use.

Risk: Runtime npx resolution can execute an unreviewed or changed agent-browser package.

Mitigation: Prefer a pinned or reviewed agent-browser installation before running automation commands.

## Reference(s):

- [Daxiang Electron on ClawHub](https://clawhub.ai/daxiangnaoyang/skills/daxiang-electron)
- [daxiangnaoyang Publisher Profile](https://clawhub.ai/user/daxiangnaoyang)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide an agent to launch Electron apps with remote debugging enabled and control authenticated desktop app sessions through local CDP ports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
