## Description:

Automates browser tasks from the command line with browser-use, including navigation, interaction, screenshots, tabs, cookies, JavaScript, cloud browsing, and local tunneling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zdstudios](https://clawhub.ai/user/zdstudios)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to drive browser-use CLI workflows for web navigation, inspection, form interaction, screenshots, JavaScript execution, cookie and tab management, cloud browser sessions, and local app testing through tunnels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users to run remote installer code.

Mitigation: Install only when the browser-use publisher is trusted; prefer an isolated Python environment and manual installation when stronger review is needed.

Risk: Browser automation can access pages, cookies, and local browser profiles.

Mitigation: Use a dedicated low-privilege browser profile and avoid syncing personal or work profiles.

Risk: Cloud browser and tunnel workflows can expose local services or sensitive browsing state.

Mitigation: Avoid public tunnels for sensitive local apps, and close daemons, tunnels, and cloud browsers when work is complete.

Risk: Diagnostics, screenshots, logs, and exported cookies may contain sensitive data.

Mitigation: Redact diagnostic output and generated files before sharing or storing them outside the trusted workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zdstudios/skills/browser-cli)
- [Publisher profile](https://clawhub.ai/user/zdstudios)
- [browser-use CLI installer](https://browser-use.com/cli/install.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration paths, and command recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that start daemon sessions, use browser profiles, manage cookies, call cloud APIs, or open public tunnels.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
