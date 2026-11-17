## Description:

Climb the browser ladder - start free, escalate only when needed. L1 (fetch) to L2 (local Playwright) to L3 (BrowserCat) to L4 (Browserless.io for CAPTCHA/bot bypass).

This skill is ready for commercial/non-commercial use.

## Publisher:

[ktpriyatham](https://clawhub.ai/user/ktpriyatham)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to choose a browser access method for URL retrieval, JavaScript rendering, screenshots, PDFs, cloud browser fallback, and authorized CAPTCHA or bot-detection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party cloud browser providers may receive requested URLs and page data.

Mitigation: Avoid private sessions, internal URLs, authenticated pages, and sensitive content unless use is explicitly authorized and provider risk has been reviewed.

Risk: The skill normalizes CAPTCHA and bot-detection bypass workflows.

Mitigation: Use CAPTCHA or bot bypass only with explicit authorization and in compliance with the target site's rules and applicable policy.

Risk: Browser execution uses Docker and mutable external tooling.

Mitigation: Review commands before execution, pin trusted images or dependencies where possible, and run browser automation in an isolated environment.

Risk: Optional provider tokens are stored in a local .env file.

Mitigation: Protect the .env file, avoid committing credentials, and rotate tokens if exposure is suspected.

## Reference(s):

- [BrowserCat](https://browsercat.com)
- [Browserless.io](https://browserless.io)
- [Browser Ladder on ClawHub](https://clawhub.ai/ktpriyatham/skills/browser-ladder)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with bash and JavaScript examples; helper scripts may emit HTML, screenshots, PDFs, or status messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Optional BrowserCat and Browserless.io credentials enable cloud browser rungs; local browser execution depends on Docker.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
