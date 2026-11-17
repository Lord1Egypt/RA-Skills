## Description:

Binance Square publishing skill for AI agents. Validate session, publish posts, and check status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phlegonlabs](https://clawhub.ai/user/phlegonlabs)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to validate a Binance Square session, publish posts, and check post status from structured inputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires live Binance browser-session credentials and can publish publicly on the connected account.

Mitigation: Use an isolated or test account where possible, validate the session before publishing, and review each post payload before execution.

Risk: Credential material could be exposed if cookies, CSRF tokens, session tokens, or authorization headers are logged or sent to an untrusted destination.

Mitigation: Keep credentials out of shared files and logs, send Binance authentication only to https://www.binance.com or trusted *.binance.com endpoints, and use sanitized error output.

Risk: Analyzer, endpoint-probing, or CDP modes can broaden account access beyond a simple publish operation.

Mitigation: Avoid running analyzer or endpoint probes against a real account, and restrict CDP configuration to a local trusted browser endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/phlegonlabs/skills/bn-square-skill)
- [Publisher profile](https://clawhub.ai/user/phlegonlabs)
- [Project homepage](https://github.com/Phlegonlabs/bn-square-skill)
- [Cookie guide](docs/cookie-guide.md)
- [API notes](api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Structured JSON-compatible command results with concise operational guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include session validity, publish success, post identifiers, post URLs, status values, and sanitized errors.]

## Skill Version(s):

0.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
