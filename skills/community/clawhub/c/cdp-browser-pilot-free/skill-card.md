## Description: <br>
Helps an agent automate an already logged-in Edge or Chrome browser through CDP for navigation, clicking, screenshots, JavaScript execution, waits, tab inspection, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and operations teams use this skill when static fetching is insufficient, especially for JavaScript-rendered pages, authenticated browser sessions, page interaction, screenshots, and structured data extraction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can let an agent control a browser session that is already logged in. <br>
Mitigation: Use a separate browser profile, low-privilege accounts, and avoid sensitive sites. <br>
Risk: Remote debugging can expose broad browser control when used with important accounts or exposed beyond the local machine. <br>
Mitigation: Do not expose the debugging port broadly; close or restart the browser session after tasks. <br>
Risk: Screenshots, exports, cookie handling, and scheduled monitoring can capture sensitive information. <br>
Mitigation: Review outputs and task scope before running automation, especially on authenticated pages. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/cdp-browser-pilot-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline PowerShell and JavaScript examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce screenshots as PNG/base64 and extracted page data as strings or JSON when the browser automation module is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
