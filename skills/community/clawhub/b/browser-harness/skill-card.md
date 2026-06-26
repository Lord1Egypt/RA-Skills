## Description: <br>
Controls a local Edge or Chrome browser through CDP to open pages, capture screenshots, extract rendered page content, and automate browser actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[19770117](https://clawhub.ai/user/19770117) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs to inspect JavaScript-rendered pages, capture browser screenshots, extract page text, or drive a user-approved local browser session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent broad control over a real browser session. <br>
Mitigation: Use a dedicated temporary browser profile, avoid sensitive or logged-in sites unless explicitly approved, and close the debug-enabled browser when finished. <br>
Risk: The remote browser option is under-explained and may expose page content or credentials outside the local environment. <br>
Mitigation: Do not enable remote or cloud mode unless the operator has reviewed the external browser-harness project and understands where browser data may be sent. <br>
Risk: The skill requires sensitive browser and API-key configuration. <br>
Mitigation: Set credentials only for the intended session and review commands before execution. <br>


## Reference(s): <br>
- [Browser Harness project](https://github.com/browser-use/browser-harness) <br>
- [ClawHub skill page](https://clawhub.ai/19770117/browser-harness) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and browser automation snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser screenshots or extracted page content through the browser-harness CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
