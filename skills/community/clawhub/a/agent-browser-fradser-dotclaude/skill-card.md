## Description: <br>
Browser automation command reference and usage patterns for web testing, form filling, screenshots, and data extraction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jsafe](https://clawhub.ai/user/jsafe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill as a browser automation reference for navigating sites, interacting with forms, capturing screenshots, managing sessions, and extracting page information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser automation can save page contents, screenshots, videos, cookies, headers, and session state that may contain sensitive information. <br>
Mitigation: Keep generated artifacts private, redact sensitive captures before sharing, and delete saved browser state when the task is complete. <br>
Risk: Automated interactions can operate in authenticated sessions and submit forms or modify browser state. <br>
Mitigation: Review target URLs and planned actions before execution, and use isolated sessions or test accounts when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jsafe/agent-browser-fradser-dotclaude) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and optional JSON-producing workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe browser artifacts such as screenshots, PDFs, videos, traces, cookies, storage, headers, and network request summaries when those documented commands are used.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
