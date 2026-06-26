## Description: <br>
Assists with CAPTCHA-protected web login workflows by using Chrome DevTools MCP screenshots, AI vision CAPTCHA recognition, and automated form submission guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leungBH](https://clawhub.ai/user/leungBH) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to guide browser-based login workflows for systems they own or are explicitly authorized to access when CAPTCHA verification is present. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates CAPTCHA-protected login and password submission, which can be misused or violate site anti-automation rules. <br>
Mitigation: Use it only on systems the operator owns or is explicitly authorized to automate, confirm each target URL and form submission manually, and avoid bypassing site anti-automation rules. <br>
Risk: Login screenshots and credentials may expose sensitive information. <br>
Mitigation: Do not paste real passwords into reusable scripts, avoid logging credentials, and delete saved login screenshots after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leungBH/captcha-login-assistant) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code] <br>
**Output Format:** [Markdown with JavaScript and MCP command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser automation steps that handle credentials and CAPTCHA screenshots; use only with explicit authorization.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
