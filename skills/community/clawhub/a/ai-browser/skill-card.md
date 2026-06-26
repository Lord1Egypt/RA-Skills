## Description: <br>
AI Browser lets an agent control a Chromium browser over WebSocket for navigation, clicking, typing, screenshots, DOM snapshots, JavaScript evaluation, and status checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linbo405](https://clawhub.ai/user/linbo405) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to run a local browser-control service for web testing, data collection, screenshots, form filling, and site monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated browser-control access can allow connected clients to read page contents, capture screenshots, collect form values, type, click, and run JavaScript in the browser. <br>
Mitigation: Expose the WebSocket service and Chrome debugging port only to trusted local users or networks, block untrusted access, and avoid sensitive logged-in sessions unless that level of control is intended. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linbo405/ai-browser) <br>
- [Publisher profile](https://clawhub.ai/user/linbo405) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON WebSocket responses, base64 screenshots, and Markdown usage guidance with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Screenshots are returned as base64 image data; browser actions can read page content and interact with live pages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
