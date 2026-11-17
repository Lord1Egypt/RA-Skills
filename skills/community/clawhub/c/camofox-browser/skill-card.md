## Description:

Headless browser server enabling AI agents to create tabs, navigate, interact, and capture snapshots with element references locally or in the cloud.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sheffk78](https://clawhub.ai/user/sheffk78)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give AI agents a local or cloud-hosted anti-detection browser API for web navigation, page snapshots, element interaction, screenshots, downloads, cookie import, proxies, and YouTube transcript extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent-controlled anti-detection browsing can be misused or can access sensitive web sessions.

Mitigation: Install only for intentional browser automation use cases and avoid importing cookies for sensitive accounts.

Risk: Exposing the browser server publicly can expand access to powerful browser, session, cookie, and JavaScript controls.

Mitigation: Keep the server bound to localhost or a private trusted network, do not expose port 9377 publicly, and set strong CAMOFOX_API_KEY and CAMOFOX_ADMIN_KEY values.

Risk: Page JavaScript evaluation can run code in the browser page context.

Mitigation: Restrict use of camofox_evaluate and review tasks that request arbitrary JavaScript execution.

Risk: Outdated dependencies or browser artifacts can increase operational and security exposure.

Mitigation: Update or pin dependencies and browser artifacts before production deployment.

## Reference(s):

- [Camofox Browser on ClawHub](https://clawhub.ai/sheffk78/skills/camofox-browser)
- [Camoufox](https://camoufox.com)
- [OpenClaw](https://openclaw.ai)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON API responses, shell commands, screenshots, and text snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include accessibility snapshots with element refs, base64 screenshots or downloads, imported cookie status, and transcript text depending on the invoked tool.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
