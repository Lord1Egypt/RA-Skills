## Description: <br>
Captcha Base Skill provides free-first CAPTCHA solving with local recognition and optional low-cost JFBYM cloud fallback for OpenClaw/ClawHub, browser automation, and RPA workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaoqf-cq](https://clawhub.ai/user/zhaoqf-cq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation engineers use this skill to solve text, math, and slider CAPTCHAs locally first, with optional JFBYM fallback for complex challenges such as click-selection, rotation, ReCAPTCHA, hCaptcha, or Turnstile when they are authorized to automate the workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud solving can send supplied CAPTCHA images, challenge metadata such as page URLs or site keys, and the configured JFBYM token to JFBYM. <br>
Mitigation: Use local-only operation by leaving JFBYM_TOKEN unset when cloud processing is not needed, and avoid sending sensitive screenshots or unauthorized challenges to the cloud provider. <br>
Risk: Cloud fallback can incur third-party usage charges when enabled. <br>
Mitigation: Configure JFBYM_TOKEN only in controlled environments, limit retry behavior, and monitor account balance before broad automation runs. <br>
Risk: CAPTCHA automation may be inappropriate outside workflows the user is permitted to automate. <br>
Mitigation: Use the skill only for authorized CAPTCHA workflows and confirm that the target service permits the intended automation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaoqf-cq/captcha-base-skill) <br>
- [ddddocr project](https://github.com/sml2h3/ddddocr) <br>
- [JFBYM pricing](https://www.jfbym.com/price.html) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON objects from CLI calls and Python strings or dictionaries from library calls, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local mode processes supplied images without cloud upload; cloud mode can return provider-specific result fields and fallback metadata.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
