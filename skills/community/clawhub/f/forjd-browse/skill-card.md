## Description: <br>
Browse is a browser automation CLI for AI agents that helps navigate pages, fill forms, click buttons, take screenshots, extract data, test web apps, and automate browser tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danjdewhurst](https://clawhub.ai/user/danjdewhurst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and agents use Browse to automate real browser workflows for navigation, form input, UI testing, screenshots, accessibility checks, performance checks, data extraction, and session-based web interactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control logged-in browser sessions through a local `browse` command. <br>
Mitigation: Install it only when the local `browse` CLI is trusted, use test accounts or isolated sessions where possible, and confirm before sensitive submissions or account changes. <br>
Risk: Saved authentication state may expose cookies, tokens, or other session secrets. <br>
Mitigation: Treat auth-state files as secrets and run `browse wipe` or close sessions after sensitive browsing. <br>
Risk: Broad browser automation can perform unintended actions when instructions are vague. <br>
Mitigation: Use narrow, explicit instructions and require confirmation before uploads, purchases, public posts, webhook reporting, or other externally visible actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danjdewhurst/forjd-browse) <br>
- [Publisher profile](https://clawhub.ai/user/danjdewhurst) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance] <br>
**Output Format:** [Plain text and Markdown with inline shell commands and JSON-stringified command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may create screenshots, traces, videos, reports, auth-state files, and other browser automation artifacts when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
