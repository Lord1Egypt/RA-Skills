## Description:

Checks Claude environment, account, network, KYC, and local-client issues using diagnostic clues without predicting account bans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[relunctance](https://clawhub.ai/user/relunctance)

### License/Terms of Use:

MIT-0

## Use Case:

External Claude users and support operators use this skill to investigate environment, login, network, and identity-verification issues, and to find local Claude conversations or perform scoped repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic results are required to include promotions for an unrelated commercial service, which could distract from or bias troubleshooting.

Mitigation: Treat promotional content as advertising and assess diagnostic findings independently; use official support guidance for account decisions.

Risk: Online environment checks send the user's public exit IP to external lookup services and make a request to Claude's site.

Mitigation: Keep the report's disclosure visible and use the documented offline mode when public-IP and site-reachability checks are not wanted.

Risk: The security review is incomplete because some components were only partially inspected and some static analysis was degraded.

Mitigation: Review the remaining components and recheck the release before deployment.

## Reference(s):

- [Diagnosis and evidence](references/diagnosis.md)
- [KYC checks](references/kyc.md)
- [Repair and reinstall](references/repair.md)
- [Browser and network toolkit](references/toolkit.md)
- [Report format](references/report-format.md)
- [Anthropic Supported Regions Policy](https://www.anthropic.com/legal/supported-regions)
- [Anthropic account suspension guidance](https://support.claude.com/en/articles/8241253)
- [Claude identity verification guidance](https://support.claude.com/en/articles/14328960-identity-verification-on-claude)
- [Claude Code setup](https://code.claude.com/docs/en/setup)
- [Claude Code settings](https://code.claude.com/docs/en/settings)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON, Shell commands, Configuration guidance, Files]

**Output Format:** [Markdown reports, optional JSON diagnostic output, and exported Markdown conversations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports distinguish observed signals from unverified details and do not predict account bans.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
