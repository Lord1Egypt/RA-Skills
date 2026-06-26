## Description: <br>
Guide for AI agents on how to use Chrome Remote Debugging on port 9222 to automate browser interactions, including connecting, navigating, taking screenshots, reading page structure, clicking, typing, scrolling, executing JavaScript, and handling common pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lgx-00](https://clawhub.ai/user/lgx-00) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to control Chrome through the Chrome DevTools Protocol when a task requires authenticated browser sessions, JavaScript-rendered pages, visual inspection, or multi-step page interaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to control logged-in Chrome sessions through remote debugging. <br>
Mitigation: Use a separate low-privilege browser profile, close unrelated tabs, and avoid sensitive pages. <br>
Risk: Browser actions could submit forms, change settings, post content, purchase items, delete data, save or share screenshots, or run JavaScript on authenticated sites. <br>
Mitigation: Require explicit confirmation before any high-impact browser action or JavaScript execution on authenticated sites. <br>
Risk: Screenshots and page snapshots can expose authenticated or sensitive page content. <br>
Mitigation: Capture and share only the minimum browser state needed for the task. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/lgx-00/chrome-remote-browser) <br>
- [Publisher profile](https://clawhub.ai/user/lgx-00) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, code] <br>
**Output Format:** [Markdown with JSON examples, shell command snippets, and JavaScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only guide for browser automation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
