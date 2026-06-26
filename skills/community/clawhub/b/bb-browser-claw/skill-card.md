## Description: <br>
Automates a real Chromium browser through Chrome DevTools Protocol using the bb-browser daemon and site adapters for web, social, research, finance, translation, and browser-control tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chatgptnexus](https://clawhub.ai/user/chatgptnexus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to retrieve, inspect, and act on web content through an existing logged-in Chromium session when API-based access is unavailable or insufficient. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control a real logged-in browser session, including JavaScript execution, screenshots, network capture, and actions on authenticated sites. <br>
Mitigation: Install only when the bb-browser daemon, binary, and extension are trusted; use a dedicated low-privilege browser profile and require explicit confirmation before sensitive browser actions. <br>
Risk: Site adapters may interact with platforms that use anti-bot controls or require active user sessions. <br>
Mitigation: Use the skill within each site's permitted usage, keep manual captcha or login resolution under user control, and avoid sensitive accounts in the controlled browser profile. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chatgptnexus/bb-browser-claw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and code examples; bb-browser commands can return text, screenshots, page snapshots, network data, or JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require a host bb-browser daemon, browser extension, and active logged-in Chromium session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
