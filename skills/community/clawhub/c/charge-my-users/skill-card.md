## Description:

Guides developers through configuring a deployed app to bill logged-in end users per use through SettleMesh payer sessions, quote checks, charge capture, and billing error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[structureintelligence](https://clawhub.ai/user/structureintelligence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after deployment to route paid platform calls to the logged-in end user's wallet instead of the developer's wallet. It helps implement payer forwarding, quote-before-charge flows, exact charge display, preflight testing, and billing error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill involves payment-related billing flows through SettleMesh.

Mitigation: Install and run it only after reviewing the release, confirming intended billing behavior, and keeping payment-affecting actions behind explicit user confirmation.

Risk: The skill requires the settlemesh CLI and may lead to an unpinned global CLI installation.

Mitigation: Pin the settlemesh CLI version where possible and review the package before global installation.

Risk: The skill can initiate login, session caching, spending, or credential-lending steps.

Mitigation: Set SETTLE_API_KEY only at runtime and require explicit confirmation before login, cached-session use, spending, or credential-lending actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/structureintelligence/skills/charge-my-users)
- [StructureIntelligence ClawHub profile](https://clawhub.ai/user/structureintelligence)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code]

**Output Format:** [Markdown with inline shell commands and HTTP request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the settlemesh CLI and SETTLE_API_KEY; networked billing, login, session caching, spending, and credential-lending steps should be reviewed and explicitly confirmed.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
