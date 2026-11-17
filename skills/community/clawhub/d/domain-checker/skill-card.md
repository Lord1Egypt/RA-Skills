## Description:

Check whether domain names are available for registration using WHOIS and DNS cross-verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blueyi](https://clawhub.ai/user/blueyi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and naming teams use this skill to check candidate domain names and summarize whether they appear available, taken, likely taken, or unknown before manual registrar confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WHOIS and DNS checks make outbound queries that may disclose candidate domains to external infrastructure.

Mitigation: Avoid checking confidential names on unapproved networks and use trusted domain inputs where possible.

Risk: Malformed or machine-supplied domain strings can affect displayed terminal output.

Mitigation: Review or normalize domain inputs before running checks and treat generated output as informational.

Risk: Availability signals may not reflect premium pricing, aftermarket listings, or final registrar purchase status.

Mitigation: Confirm availability and pricing with a registrar before acting on a result.

## Reference(s):

- [Domain Checker ClawHub release page](https://clawhub.ai/blueyi/skills/domain-checker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown or plain text with command examples and domain availability verdicts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are advisory and should be confirmed with a registrar before purchase decisions.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
