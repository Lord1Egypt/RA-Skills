## Description: <br>
Controls a local headless Chrome browser with Selenium for page navigation, element interaction, screenshots, cookies, tabs, JavaScript execution, proxy settings, and page inspection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tr0812](https://clawhub.ai/user/tr0812) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation-focused agent users use this skill to drive a local headless Chrome session for web navigation, form interaction, screenshots, link and image extraction, cookie handling, and browser debugging tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad browser automation can access page content, cookies, screenshots, JavaScript execution, proxy configuration, and form submission on sites the agent opens. <br>
Mitigation: Use the skill only on trusted sites where automation is allowed, avoid logged-in, payment, and admin workflows unless strictly necessary, and do not share cookie, screenshot, or page-source outputs. <br>
Risk: The security summary states that the skill grants broad web-control and browser-data access without enough scoping or user safeguards. <br>
Mitigation: Review requested browser actions before running them, keep browser activity scoped to the intended task, and inspect saved screenshots in ~/Pictures/OpenClaw before reuse or disclosure. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/tr0812/browser-automation-ctrl) <br>
- [Publisher Profile](https://clawhub.ai/user/tr0812) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and shell commands, with JSON-like command results from the browser control script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create screenshot files under ~/Pictures/OpenClaw and may return page metadata, cookies, source excerpts, links, images, titles, and URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
