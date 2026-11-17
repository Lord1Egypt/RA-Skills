## Description:

Chrome Control Proxy guides agents in using a host chrome-control-proxy service to manage Chrome and run Playwright page snapshots, scripts, and pipelines over HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhengxiangqi](https://clawhub.ai/user/zhengxiangqi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to call a local Chrome Control Proxy service from a host or container, inspect page state, and execute Playwright-driven browser actions in the recommended order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs users to install a globally available npm package without a pinned version.

Mitigation: Install only a trusted, reviewed version of the package and pin the version used in controlled environments.

Risk: The Playwright run endpoint can execute powerful browser automation scripts.

Mitigation: Bind the service to localhost only and do not expose the endpoint to other users or networks.

Risk: Browser automation may interact with sensitive logged-in sessions.

Mitigation: Use a separate browser profile without sensitive active sessions for automation.

## Reference(s):

- [Chrome Control Proxy project homepage](https://github.com/zhengxiangqi/chrome-control-proxy)
- [ClawHub skill page](https://clawhub.ai/zhengxiangqi/skills/chrome-control-proxy)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, code, configuration]

**Output Format:** [Markdown with inline HTTP endpoint examples, shell commands, and Playwright script guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance includes endpoint ordering, snapshot options, target selection, timeout handling, and browser-session safety notes.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
