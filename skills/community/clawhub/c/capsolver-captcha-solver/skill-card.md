## Description:

Use CapSolver to automatically resolve Geetest, reCAPTCHA v2, reCAPTCHA v3, MTCaptcha, DataDome, AWS WAF, Cloudflare Turnstile, and Cloudflare Challenge challenges.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capsolver](https://clawhub.ai/user/capsolver)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to call the CapSolver API from an agent workflow and obtain CAPTCHA challenge solutions or tokens for supported challenge types. Users should only apply it where they are authorized to use a third-party CAPTCHA or anti-bot solving service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends CAPTCHA or anti-bot challenge material to a third-party service.

Mitigation: Use it only when authorized for the target site and when third-party processing of challenge data is acceptable.

Risk: API keys, proxy credentials, WAF tokens, returned cookies, page HTML, and challenge data are sensitive.

Mitigation: Store secrets in protected environment variables or local secret stores, avoid placing them directly in shared command histories or logs, and redact outputs before sharing.

Risk: The server security verdict is suspicious because the skill has limited safety disclosure for anti-bot solving behavior.

Mitigation: Run it in an isolated environment with reviewed dependency versions and document acceptable-use boundaries before deployment.

## Reference(s):

- [CapSolver homepage](https://capsolver.com/)
- [CapSolver documentation](https://docs.capsolver.com/)
- [CapSolver proxy usage guide](https://docs.capsolver.com/guide/api-how-to-use-proxy/)
- [ClawHub skill page](https://clawhub.ai/capsolver/skills/capsolver-captcha-solver)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; solver commands print JSON solution data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a CapSolver API key and may require proxy, site key, page HTML, image, or challenge-specific parameters depending on task type.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
