## Description: <br>
Controls user-attached Chrome tabs through a Chrome Extension relay so an agent can navigate, capture screenshots, inspect page state, click elements, fill fields, and evaluate JavaScript in the visible browser session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZaviWayne](https://clawhub.ai/user/ZaviWayne) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to operate a Chrome tab that the user has manually opened and attached, especially for browser reuse, screenshots, form entry, clicking, navigation, or page inspection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can execute arbitrary JavaScript in a user-attached Chrome tab with access to that page's live session. <br>
Mitigation: Keep the relay token private, attach only the specific tab needed, avoid sensitive logged-in pages unless necessary, and require explicit confirmation before JavaScript evaluation. <br>
Risk: Browser actions such as form fills, clicks, submissions, purchases, or account changes can have irreversible effects. <br>
Mitigation: Require explicit user confirmation before form fills, purchases, submissions, account changes, or other irreversible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZaviWayne/chrome-relay-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline shell commands, configuration snippets, and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save browser screenshots as PNG files at user-specified paths.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
