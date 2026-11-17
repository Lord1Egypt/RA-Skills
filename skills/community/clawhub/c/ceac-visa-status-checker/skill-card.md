## Description:

Automatically check U.S. visa application status in CEAC (NIV), solve CEAC captcha with Zhipu vision model, and return structured status JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xavierjiezou](https://clawhub.ai/user/xavierjiezou)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check CEAC NIV visa application status from a local environment using CEAC case details and a Zhipu API key for captcha OCR. It is intended for status lookup, monitoring, and troubleshooting when the required CEAC fields are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive passport and visa case details while submitting status checks to CEAC.

Mitigation: Enter values locally, avoid elevated privileges, and run in a dedicated virtual environment.

Risk: The CEAC captcha image is sent to Zhipu for OCR, exposing the captcha to a third-party service.

Mitigation: Use the Zhipu API key only if this third-party OCR flow is acceptable, keep the key private, and scope or rotate it according to local policy.

Risk: Unpinned dependency ranges can change behavior over time.

Mitigation: Prefer pinned dependencies or a lockfile before routine use.

## Reference(s):

- [LOCATION reference](references/LOCATION.md)
- [CEAC status tracker](https://ceac.state.gov)
- [Zhipu AI platform](https://open.bigmodel.cn/)
- [ClawHub skill page](https://clawhub.ai/xavierjiezou/skills/ceac-visa-status-checker)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and structured JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success, status, case_last_updated, description, and application_num on success; returns success false with error details on failure.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
