## Description:

Browser automation via HTTP API. Use for headless browser control, web automation, form filling, data extraction, and interactive element interaction. Supports launching instances, navigating pages, taking screenshots, extracting page structure, and clicking elements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dexifried](https://clawhub.ai/user/dexifried)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use PinchTab to control a local browser through HTTP endpoints for navigation, page snapshots, element clicks, form workflows, data extraction, and screenshot capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bundled browser-control token could allow unintended access to the local PinchTab service if reused.

Mitigation: Replace and rotate the embedded token before use, and load per-user secrets from environment variables or a secret store.

Risk: Screenshot capture, local persistence, and Telegram export can expose credentials, account data, private messages, or internal information from browser pages.

Mitigation: Use screenshot and Telegram workflows only on pages whose contents are approved for export, and avoid sensitive browsing sessions unless export is explicitly intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dexifried/skills/dexifried-pinchtab)
- [API Endpoints](references/api-endpoints.md)
- [Common Workflows](references/common-workflows.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce browser snapshots, screenshot files, and optional Telegram photo messages when the user runs the bundled scripts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
