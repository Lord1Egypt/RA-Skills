## Description: <br>
Climb the browser ladder -- start free, escalate only when needed. L1 (fetch) -> L2 (local Playwright) -> L3 (BrowserCat) -> L4 (Browserless.io for CAPTCHA/bot bypass). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ktpriyatham](https://clawhub.ai/user/ktpriyatham) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to choose the least expensive browser access path that can handle a target URL, from static fetches through local Playwright and optional cloud browser services. It is useful for page loading checks, rendered HTML retrieval, screenshots, and PDFs when the operator has approved the necessary local or cloud rung. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud browser rungs can send requested URLs and page interaction context to third-party services. <br>
Mitigation: Use local rungs for sensitive, internal, or authenticated pages unless BrowserCat or Browserless.io has been approved for that data. <br>
Risk: Level 4 normalizes CAPTCHA or bot-detection bypass and may create policy or site-terms risk. <br>
Mitigation: Configure BROWSERLESS_TOKEN only when paid cloud bypass behavior is explicitly intended and appropriate for the target site. <br>
Risk: Automatic escalation can use a paid cloud browser when lower rungs fail. <br>
Mitigation: Force a lower rung with --level when cost, bypass behavior, or third-party rendering is not appropriate. <br>


## Reference(s): <br>
- [Browser Ladder on ClawHub](https://clawhub.ai/ktpriyatham/browser-ladder) <br>
- [BrowserCat](https://browsercat.com) <br>
- [Browserless.io](https://browserless.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell and JavaScript examples; browse.sh can return status text, HTML, screenshots, or PDFs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local Docker or optional BrowserCat and Browserless.io credentials depending on the selected rung.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
