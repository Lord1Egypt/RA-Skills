## Description:

Solve CAPTCHAs (reCAPTCHA v2/v3, hCaptcha, Cloudflare Turnstile, image CAPTCHAs) using CapMonster Cloud API. Use when browser automation encounters CAPTCHA challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[easonc13](https://clawhub.ai/user/easonc13)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to detect CAPTCHA challenges, submit CAPTCHA tasks to CapMonster Cloud, poll for a solution token, and inject the token into a browser workflow when they are authorized to automate the target site.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be used to bypass anti-abuse checks on arbitrary websites.

Mitigation: Use it only for sites and workflows where CAPTCHA solving and automation are explicitly authorized.

Risk: Target URLs, sitekeys, and the CapMonster API key are sent to CapMonster Cloud.

Mitigation: Review data-sharing requirements before use and store CAPMONSTER_API_KEY as a managed secret.

Risk: Automated solves may incur usage charges.

Mitigation: Set account spending limits, monitor balance, and scope automation volume before running at scale.

## Reference(s):

- [CapMonster Cloud documentation](https://docs.capmonster.cloud/)
- [CapMonster Cloud API endpoint](https://api.capmonster.cloud)
- [ClawHub skill page](https://clawhub.ai/easonc13/skills/capmonster)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript, Python, and shell command snippets; helper scripts return status text, JSON-formatted detection results, CAPTCHA tokens, and shell exit codes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CAPMONSTER_API_KEY and sends target URLs and sitekeys to CapMonster Cloud.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
