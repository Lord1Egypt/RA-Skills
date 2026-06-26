## Description: <br>
Solve CAPTCHAs with 2Captcha from the command line during browser automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adinvadim](https://clawhub.ai/user/adinvadim) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to configure and invoke a 2Captcha CLI for authorized CAPTCHA-solving workflows during browser automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CAPTCHA content, page metadata, and challenge details are sent to 2Captcha and may be handled by human solvers. <br>
Mitigation: Use the skill only for approved workflows and avoid sensitive, regulated, internal, or third-party user data unless that data sharing is authorized. <br>
Risk: The 2Captcha API key is a paid-service credential that may be stored in an environment variable or local config file. <br>
Mitigation: Store the key with appropriate local permissions, avoid committing it, and rotate it if exposure is suspected. <br>
Risk: CAPTCHA-solving automation can violate site policies or user expectations when used without authorization. <br>
Mitigation: Confirm the target workflow permits automated CAPTCHA solving before using the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/adinvadim/2captcha) <br>
- [Publisher profile](https://clawhub.ai/user/adinvadim) <br>
- [Project homepage](https://github.com/adinvadim/2captcha-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and CLI output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can return plain text or JSON results depending on flags.] <br>

## Skill Version(s): <br>
2.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
