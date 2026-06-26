## Description: <br>
Form Auto is an OpenClaw browser automation skill that helps agents detect, fill, summarize, and confirm standard web form fields for job applications, registrations, surveys, and similar workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobewin](https://clawhub.ai/user/tobewin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and agents use this skill to gather form details, match user-provided data to fields, fill supported HTML controls, and pause for review before submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates in a logged-in browser session and may access or enter personal data on selected forms. <br>
Mitigation: Use it only on trusted websites and consider a separate browser profile for testing or lower-trust workflows. <br>
Risk: Automatically matched form fields may be incorrect or may place sensitive information in the wrong field. <br>
Mitigation: Review every filled field and the generated summary before submitting any form. <br>
Risk: Saved form templates may contain reusable personal information, while storage and deletion behavior are not fully specified by the evidence. <br>
Mitigation: Avoid storing highly sensitive data in templates and clear saved data when it is no longer needed. <br>
Risk: Payment, captcha, file-upload, or dynamically loaded forms may not be handled reliably. <br>
Mitigation: Do not use the skill for payment forms or captchas, and switch to manual review or manual entry when fields fail to load or fill correctly. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobewin/form-auto) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with JavaScript, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires OpenClaw v2026.3.22 or later with browser access and python3 available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
