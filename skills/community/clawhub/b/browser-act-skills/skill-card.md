## Description: <br>
Browser Act enables agents to use the browser-act CLI for rendered web navigation, extraction, screenshots, form workflows, session automation, and browser/session management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[browseract-cli](https://clawhub.ai/user/browseract-cli) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs full-browser automation for JavaScript-rendered pages, authenticated sessions, form workflows, screenshots, or network capture that simpler fetch tools cannot handle. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation rules could steer an agent to a powerful browser and session automation tool for ordinary web tasks. <br>
Mitigation: Review when the skill is invoked and prefer simpler read-only web tools unless browser rendering or session automation is needed. <br>
Risk: Browser automation can affect authenticated sessions or perform sensitive actions such as login, form submission, file upload, browser creation, or deletion. <br>
Mitigation: Keep explicit confirmation prompts enabled for sensitive operations and review proposed browser actions before execution. <br>


## Reference(s): <br>
- [Browser Act homepage](https://www.browseract.com) <br>
- [ClawHub Browser Act skill page](https://clawhub.ai/browseract-cli/browser-act-skills) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline browser-act CLI commands and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser workflow guidance, confirmation requirements, installation commands, and session-management instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
