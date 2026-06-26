## Description: <br>
A visual, human-like web browser for OpenClaw agents that supports reading pages, screenshots, and visible mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Canbirlik](https://clawhub.ai/user/Canbirlik) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when an OpenClaw agent needs a real Chromium browser to read JavaScript-rendered pages, capture screenshots, or run in visible mode for web tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill lets an agent drive a real browser, including pages that may contain sensitive local, intranet, account, or credential data. <br>
Mitigation: Use it only on sensitive pages when that access is explicitly intended, and prefer non-sensitive browsing contexts for routine tasks. <br>
Risk: The setup flow installs Playwright's Chromium browser binary before use. <br>
Mitigation: Review the browser-binary installation step before running it in the target environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Canbirlik/claw-browser) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files, guidance] <br>
**Output Format:** [Console text and optional PNG screenshot file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The read action prints a page title and up to 5000 characters of body text; the screenshot action writes evidence.png.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
