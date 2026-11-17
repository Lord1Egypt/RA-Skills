## Description:

Provides local-first CAPTCHA recognition with optional JFBYM cloud fallback for text, arithmetic, slider, selection, rotation, ReCAPTCHA, hCaptcha, and related challenge workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoqf-cq](https://clawhub.ai/user/zhaoqf-cq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to add CAPTCHA handling to OpenClaw, ClawHub, browser automation, RPA, and data-collection workflows. It supports local OCR for simpler challenges and optional paid cloud solving for more complex CAPTCHA types.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cloud mode or automatic fallback can send CAPTCHA images, challenge metadata, and the JFBYM token to a third-party paid solver.

Mitigation: Use local-only mode by keeping JFBYM_TOKEN unset unless third-party processing is acceptable for the specific workflow.

Risk: Screenshots or CAPTCHA images may contain sensitive information beyond the challenge itself.

Mitigation: Crop inputs to the CAPTCHA area and avoid submitting full-page or privacy-sensitive screenshots to cloud solving.

Risk: Pinned image-processing dependencies process untrusted image data.

Mitigation: Run the skill in an isolated environment and upgrade pinned dependencies before processing untrusted images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaoqf-cq/skills/captcha-base-skill)
- [JFBYM console](https://console.jfbym.com/register/TG133710)
- [JFBYM pricing](https://www.jfbym.com/price.html)
- [ddddocr project](https://github.com/sml2h3/ddddocr)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [Python return values and CLI JSON output, with Markdown usage guidance and shell commands in documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include recognized text, arithmetic results, slider coordinates, cloud solver response data, account balance data, or recommended JFBYM CAPTCHA type codes.]

## Skill Version(s):

1.0.10 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
