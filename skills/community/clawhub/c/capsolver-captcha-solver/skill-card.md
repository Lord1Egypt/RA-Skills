## Description: <br>
Use capsolver to automatically resolve Geetest, reCAPTCHA v2, reCAPTCHA v3, MTCaptcha, DataDome, AWS WAF, Cloudflare Turnstile, and Cloudflare Challenge, etc. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[capsolver](https://clawhub.ai/user/capsolver) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to call CapSolver for CAPTCHA recognition and token-solving workflows in authorized RPA or browser automation contexts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides broad CAPTCHA and anti-bot bypass capability. <br>
Mitigation: Use it only for authorized target sites and review whether the workflow complies with site rules and organizational policy before deployment. <br>
Risk: The skill can send challenge data, proxy values, page URLs, user-agent values, and page HTML to CapSolver. <br>
Mitigation: Avoid sending private page HTML, account data, session data, or other sensitive content; treat API_KEY and proxy credentials as secrets. <br>
Risk: The security scan verdict is suspicious. <br>
Mitigation: Require security review and intentional approval before installation in production automation. <br>


## Reference(s): <br>
- [CapSolver Homepage](https://capsolver.com/) <br>
- [ImageToTextTask Documentation](https://docs.capsolver.com/en/guide/recognition/ImageToTextTask/#independent-module-support) <br>
- [reCAPTCHA Classification Documentation](https://docs.capsolver.com/guide/recognition/ReCaptchaClassification/) <br>
- [AWS WAF Classification Documentation](https://docs.capsolver.com/guide/recognition/AwsWafClassification/) <br>
- [VisionEngine Documentation](https://docs.capsolver.com/guide/recognition/VisionEngine/) <br>
- [Proxy Usage Documentation](https://docs.capsolver.com/guide/api-how-to-use-proxy/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Configuration] <br>
**Output Format:** [JSON responses from CapSolver API calls, with command-line usage guidance in Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API_KEY secret and may accept proxy, user-agent, page URL, challenge HTML, site key, image, or token parameters depending on the task type.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
