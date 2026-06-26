## Description: <br>
Browser Automation helps an agent control a real signed-in Chrome or Chromium browser through browser-relay-cli and the Browser Relay extension for tab, page, click, typing, scroll, screenshot, and visible-content workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jasoncodespace](https://clawhub.ai/user/jasoncodespace) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a task needs local browser control in a real Chrome or Chromium session, including signed-in pages, tab reuse, DOM-first actions, and screenshot-guided fallback when selectors are unreliable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate inside a signed-in Chrome session. <br>
Mitigation: Use a separate Chrome profile or test account when practical, avoid sensitive pages unless necessary, and confirm purchases, posts, deletions, and account changes before they happen. <br>
Risk: The Browser Relay workflow exposes broad browser-control and raw passthrough commands. <br>
Mitigation: Review commands before execution, prefer DOM-first actions, and use raw passthrough only when it is necessary for the task. <br>
Risk: The workflow depends on the browser-relay-cli package and an unpacked browser extension. <br>
Mitigation: Install only if the package and extension are trusted, then disable the extension and stop the relay after use. <br>


## Reference(s): <br>
- [Browser Relay Commands](references/commands.md) <br>
- [Browser Relay GitHub Repository](https://github.com/jasonCodeSpace/browser-relay) <br>
- [ClawHub Skill Page](https://clawhub.ai/jasoncodespace/browser-automation-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Browser Relay CLI commands that operate on local Chrome tabs and visible page state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
