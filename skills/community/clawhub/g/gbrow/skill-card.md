## Description:

Full-featured headless browser for OpenClaw agents that can navigate pages, read accessibility-tree snapshots, click by @ref, manage tabs, execute JavaScript, and import cookies without a vision model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ashish797](https://clawhub.ai/user/ashish797)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Gbrow to let OpenClaw agents browse, inspect, and interact with web pages through a local Playwright-backed browser server without relying on vision-model page reads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The local browser controller can manipulate pages, handle cookies, upload local files on command, and start a Claude CLI helper.

Mitigation: Install only in trusted environments, avoid using cookie import or saved browser state for sensitive accounts, and limit the tool to accounts and files acceptable for local automation.

Risk: The install path uses scripts and dependencies that require review before execution.

Mitigation: Review and pin setup scripts and dependencies before installing, and avoid one-line shell installers for production or sensitive environments.

Risk: The security verdict is suspicious because browser automation capabilities are under-disclosed relative to their access power.

Mitigation: Review the ClawHub security summary and guidance before deployment, then scan and test the skill under the intended permission model.

## Reference(s):

- [Gbrow ClawHub Skill Page](https://clawhub.ai/ashish797/skills/gbrow)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [Playwright](https://playwright.dev/)
- [Bun](https://bun.sh/)
- [gstack](https://github.com/garrytan/gstack)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files]

**Output Format:** [Structured text, JSON command responses, Markdown guidance, screenshots, and PDF files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are generated from browser commands and may include page text, accessibility snapshots, element references, HTML, links, forms, screenshots, or PDFs.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
