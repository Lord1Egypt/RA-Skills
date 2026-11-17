## Description:

Captcha Auto recognizes, fills, and submits webpage captchas using browser automation, full-page screenshots, and a configurable vision model endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[annoyingc](https://clawhub.ai/user/annoyingc)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation users use this skill to recognize captchas in web workflows and, when appropriate, fill the detected code into the page. It is best suited to trusted pages where full-page screenshots and automated submission are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full-page screenshots may include sensitive page content and are sent to the configured vision API endpoint.

Mitigation: Use the skill only on trusted captcha pages that do not contain passwords, payment data, personal information, or account data.

Risk: The configured vision API key is used during recognition.

Mitigation: Use a dedicated low-privilege API key, provide it through environment or local configuration, and avoid sharing workspace files that may contain configuration.

Risk: The skill can fill arbitrary form fields and click submit or login-style buttons automatically.

Mitigation: Run it in an isolated browser profile or workspace, verify the target URL first, and avoid workflows where an automatic submission could create account, payment, or data-change side effects.

## Reference(s):

- [Captcha Auto ClawHub listing](https://clawhub.ai/annoyingc/skills/captcha-auto)
- [DashScope compatible-mode API endpoint](https://dashscope.aliyuncs.com/compatible-mode/v1)
- [Google Chrome download](https://www.google.com/chrome/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, files, configuration guidance]

**Output Format:** [CLI text or JSON result with recognized captcha text, recognition method, status, screenshot paths, and run metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes full-page screenshot files to the OpenClaw workspace and may fill inputs and click submit-style buttons in the browser session.]

## Skill Version(s):

1.0.7 (source: package.json, _meta.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
