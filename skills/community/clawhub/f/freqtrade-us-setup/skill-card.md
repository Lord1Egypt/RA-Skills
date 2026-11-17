## Description:

A setup guide for configuring Freqtrade with Docker, choosing a US-compatible exchange, protecting API credentials, and starting with dry-run testing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[djc00p](https://clawhub.ai/user/djc00p)

### License/Terms of Use:

MIT-0

## Use Case:

US-based developers and traders use this guide to set up Freqtrade with Docker, configure exchange credentials, and begin with simulated trading. It also provides exchange comparison and security checklists.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: Live trading can cause losses even when API withdrawal permission is disabled.

Mitigation: Keep dry-run enabled until deliberately choosing live trading; start with conservative exposure and monitor activity.

Risk: Exposed exchange credentials could allow unauthorized trading.

Mitigation: Keep secrets in a protected, untracked file or secrets manager, disable withdrawal permission, and rotate credentials if exposed.

Risk: External Freqtrade code and the final deployment configuration are outside this guide's review.

Mitigation: Pin and review the release and image digest, protect credentials, and review the final Compose restart settings.

## Reference(s):

- [Exchange comparison](references/exchange-comparison.md)
- [Security checklist](references/security-checklist.md)
- [Freqtrade documentation](https://www.freqtrade.io)
- [Kraken API key security guidance](https://support.kraken.com/articles/api-key-security)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with shell commands and YAML/JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes setup, credential protection, exchange comparison, and dry-run guidance.]

## Skill Version(s):

1.0.5 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
