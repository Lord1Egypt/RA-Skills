## Description:

Security research proof of concept that presents a BitoPro spot-market API wrapper with public market-data tools and private account or trading tools that request BitoPro credentials.

This skill is for research and development only.

## Publisher:

[mahetagaurang22](https://clawhub.ai/user/mahetagaurang22)

### License/Terms of Use:

MIT-0

## Use Case:

Security reviewers and developers use this skill as a research artifact to understand a ClawHub slug-takeover risk involving a BitoPro-looking spot-trading integration. It should not be used for live trading, account access, or credential handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package presents itself as a BitoPro trading integration while evidence identifies it as a slug-takeover proof of concept.

Mitigation: Treat it as a security research artifact only and install publisher-verified packages for trading or account workflows.

Risk: Private account and trading actions require sensitive BitoPro API credentials.

Mitigation: Do not enter real BitoPro API keys or secrets; revoke credentials already supplied to this package.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mahetagaurang22/skills/bitopro-spot)
- [Publisher profile](https://clawhub.ai/user/mahetagaurang22)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown or text guidance with tool and credential configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May request BitoPro API key, API secret, and registered email environment variables for private account or trading actions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
