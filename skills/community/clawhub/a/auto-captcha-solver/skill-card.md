## Description: <br>
Detects and solves simple image captchas during Playwright, Puppeteer, or Selenium browser automation using preprocessing, OCR, optional arithmetic handling, input fill, and submit helpers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cx6226301](https://clawhub.ai/user/cx6226301) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and QA engineers use this skill to handle simple text or arithmetic CAPTCHA steps in browser automation for systems they own, administer, or are explicitly authorized to test. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: CAPTCHA solving can be misused against third-party anti-bot controls. <br>
Mitigation: Use only on systems you own, administer, or are explicitly authorized to test, and do not use it against third-party anti-bot controls. <br>
Risk: Browser helpers can submit forms automatically when autoSubmit is not set to false. <br>
Mitigation: Set autoSubmit to false unless deliberate form submission is intended and reviewed. <br>
Risk: The optional fallbackVision hook may send CAPTCHA images to an external provider. <br>
Mitigation: Do not configure fallbackVision with an external provider unless that data sharing is approved. <br>
Risk: OCR output can be incorrect, especially for distorted or unsupported CAPTCHA types. <br>
Mitigation: Use confidence and debug candidates for review, and avoid automatic submission in low-confidence workflows. <br>


## Reference(s): <br>
- [README](README.md) <br>
- [ClawHub skill page](https://clawhub.ai/cx6226301/auto-captcha-solver) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [JavaScript modules with JSON-like result objects and browser automation guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns solved status, value, captcha type, confidence, hash, and cache metadata when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
