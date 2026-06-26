## Description: <br>
Captcha Auto automates CAPTCHA recognition, form filling, and submission for web pages using local Tesseract OCR with fallback to a configured vision model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AnnoyingC](https://clawhub.ai/user/AnnoyingC) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation engineers use this skill to recognize CAPTCHA text on web pages, fill matching form fields, and submit the page during authorized browser automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full-page screenshots can be sent to a third-party vision API and may include passwords, account data, or personal information. <br>
Mitigation: Use only on authorized CAPTCHA pages, avoid sensitive pages, and prefer cropping to the CAPTCHA region before sending images to the vision API. <br>
Risk: The skill can automatically submit arbitrary web forms without a confirmation step. <br>
Mitigation: Require operator confirmation before submission or restrict use to test and authorized workflows where automated form submission is expected. <br>
Risk: Use of CAPTCHA automation can violate site rules or applicable policy when not explicitly authorized. <br>
Mitigation: Install and run the skill only where automation of the target site is permitted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AnnoyingC/captcha-auto) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [Human-readable terminal output or JSON with generated screenshot file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write page, filled-form, result, or error screenshots to the local workspace.] <br>

## Skill Version(s): <br>
1.0.7 (source: package.json and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
