## Description:

Detect and solve simple image captchas during browser automation for 4-6 character text, distorted alphanumeric, numeric, rotated, or arithmetic challenges that need capture, OCR, optional calculation, input fill, and submit handling in Playwright, Puppeteer, or Selenium.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cx6226301](https://clawhub.ai/user/cx6226301)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to handle simple, owned or authorized image captcha steps in browser workflows by capturing the captcha, running OCR, filling the answer, and optionally submitting the form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can bypass CAPTCHA checks and automatically submit protected forms.

Mitigation: Install it only for CAPTCHA flows you own or are explicitly authorized to test, and disable autoSubmit unless form submission is intentional.

Risk: A caller-provided fallbackVision provider may expose captcha images outside the local runtime.

Mitigation: Review and approve any fallbackVision provider before enabling it, including where image data is sent and retained.

Risk: Processing untrusted CAPTCHA images depends on image-processing and OCR libraries.

Mitigation: Update and audit the image-processing dependencies before processing untrusted images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cx6226301/skills/auto-captcha-solver)
- [Publisher profile](https://clawhub.ai/user/cx6226301)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON-compatible result objects and JavaScript browser automation helper calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns solved status, value, captcha type, confidence, hash, cache status, and optional debug candidates; browser helpers may fill inputs and submit forms.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
