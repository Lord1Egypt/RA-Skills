## Description:

Provides WebSocket control of a Chromium browser for navigation, clicking, text entry, screenshots, DOM snapshots, status checks, and script evaluation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbo405](https://clawhub.ai/user/linbo405)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to control a local Chromium browser over WebSocket for web automation, data collection, screenshots, form entry, and website monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated browser control can allow unwanted navigation, clicking, typing, screenshots, DOM access, or script evaluation if the WebSocket endpoint is reachable by an untrusted client.

Mitigation: Run the server only in an isolated environment, bind or firewall it to localhost, and add access control before exposing it beyond a trusted local process.

Risk: Screenshots, DOM snapshots, typed text, and evaluated scripts can expose private data or perform real actions on logged-in websites.

Mitigation: Avoid using sensitive logged-in browser profiles and review requested browser actions before running them against important accounts or production websites.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linbo405/skills/ai-browser-ws)
- [ClawHub publisher profile](https://clawhub.ai/user/linbo405)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON WebSocket message examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Browser responses may include JSON status data, DOM snapshots, and base64-encoded screenshots.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
