## Description: <br>
AI-powered browser automation for complex multi-step web workflows. Uses Browser-Use framework when OpenClaw's built-in browser tool can't handle login flows, anti-bot sites, or 5+ step sequences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abczsl520](https://clawhub.ai/user/abczsl520) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to automate complex browser workflows that require multiple steps, logins, anti-bot handling, or repetitive browser actions beyond a built-in browser tool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate logged-in browser sessions and submit actions on behalf of a user. <br>
Mitigation: Use a dedicated browser profile, restrict allowed domains, review generated scripts before running them, and require explicit confirmation before posting, purchasing, submitting forms, or changing account data. <br>
Risk: Page context or screenshots can be sent to the configured LLM during browser automation. <br>
Mitigation: Keep API keys in environment variables, disable vision when secrets are visible, and avoid exposing credentials or sensitive page content to the automation flow. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Python code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce browser automation scripts and setup commands for local execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
