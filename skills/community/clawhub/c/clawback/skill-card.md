## Description:

Mirror congressional stock trades with automated broker execution and risk management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mainfraame](https://clawhub.ai/user/mainfraame)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to configure, check, and run a ClawHub agent workflow that tracks congressional stock disclosures and can mirror selected trades through an E*TRADE brokerage account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real E*TRADE credentials and OAuth tokens, and the server security summary reports insecure local storage or exposure of sensitive tokens.

Mitigation: Review before installation, use sandbox accounts only until token handling is fixed, and rotate any credentials already used with this package.

Risk: The skill can execute brokerage trades, which may result in real financial loss if production credentials or account settings are used.

Mitigation: Keep setup in sandbox mode while evaluating the release, confirm account configuration and risk limits manually, and require human review before enabling live trading.

Risk: The server security guidance flags overbroad installation steps, including a sudo global symlink.

Mitigation: Inspect installation scripts before running them and avoid privileged global installation paths until the release removes or narrows those steps.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mainfraame/skills/clawback)
- [Publisher Profile](https://clawhub.ai/user/mainfraame)
- [E*TRADE Developer Portal](https://developer.etrade.com)
- [House Clerk Financial Disclosure Search](https://disclosures-clerk.house.gov)
- [Senate eFD Search](https://efdsearch.senate.gov)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with inline shell commands and configuration prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt for brokerage credentials, configuration choices, and setup confirmation before running trading commands.]

## Skill Version(s):

1.1.1 (source: server release metadata; artifact frontmatter, pyproject.toml, README, and CHANGELOG report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
