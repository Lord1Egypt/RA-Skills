## Description: <br>
Solve CAPTCHAs (reCAPTCHA v2/v3, hCaptcha, Cloudflare Turnstile, image CAPTCHAs) using CapMonster Cloud API. Use when browser automation encounters CAPTCHA challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[EasonC13](https://clawhub.ai/user/EasonC13) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation operators use this skill to detect CAPTCHA challenges, submit them to CapMonster Cloud, and apply returned tokens during browser automation on systems they own, administer, or have explicit permission to test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill automates CAPTCHA solving and token injection on live websites. <br>
Mitigation: Use it only for sites you own, administer, or have explicit permission to test, and require manual approval before sending challenge data externally, injecting tokens, invoking callbacks, or submitting live forms. <br>
Risk: The skill sends challenge data and target URLs to an external CapMonster Cloud API. <br>
Mitigation: Avoid sensitive or internal URLs and use a dedicated CapMonster API key with spending limits. <br>


## Reference(s): <br>
- [CapMonster Cloud API](https://api.capmonster.cloud) <br>
- [CapMonster Cloud Documentation](https://docs.capmonster.cloud/) <br>
- [ClawHub Skill Page](https://clawhub.ai/EasonC13/capmonster) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown with inline JavaScript, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include API calls to CapMonster Cloud and browser-token injection steps requiring manual approval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
