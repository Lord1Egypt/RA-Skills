## Description: <br>
Binance Square publishing skill for AI agents that validates sessions, publishes posts, and checks post status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phlegonlabs](https://clawhub.ai/user/Phlegonlabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use this skill to validate a Binance Square session, publish posts, and retrieve post status through structured CLI/API outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires full active Binance web-session credentials and posting authority. <br>
Mitigation: Use a dedicated low-privilege account where possible, validate the session before publishing, and keep cookies, CSRF tokens, and config files out of repositories and logs. <br>
Risk: Browser CDP, probe, and analyze scripts can inspect or exercise live Binance sessions. <br>
Mitigation: Avoid those scripts unless their side effects are understood and run them only in a controlled browser/session context. <br>
Risk: Untrusted image URLs may introduce unsafe or unexpected upload behavior. <br>
Mitigation: Pass only trusted image URLs and enforce the documented image limits before publish flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Phlegonlabs/bn-square-skill) <br>
- [Homepage](https://github.com/Phlegonlabs/bn-square-skill) <br>
- [Cookie guide](docs/cookie-guide.md) <br>
- [Messaging contract](MESSAGING.md) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Structured JSON-compatible output with concise operational text when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Binance session credentials and return sanitized errors.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata; artifact frontmatter and package.json show 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
