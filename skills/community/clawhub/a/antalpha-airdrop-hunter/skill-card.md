## Description:

Antalpha Airdrop Hunter is a Web3 airdrop assistant that grades opportunities, checks scam risk, verifies project links, and guides users toward zero-cost or current opportunities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

External Web3 users use this skill to scan airdrop opportunities, check project quality, verify suspicious URLs before wallet interaction, and get zero-cost participation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can auto-check pasted URLs through an external MCP service.

Mitigation: Do not paste signed links, password-reset links, private documents, invite URLs, internal hostnames, or URLs containing tokens or query secrets.

Risk: The skill includes multi-account or sybil-evasion guidance.

Mitigation: Treat airdrop strategy as informational and avoid tactics that violate project rules or terms.

Risk: Airdrop links and wallet interactions can expose users to phishing or asset loss.

Mitigation: Independently verify official project links before visiting sites or connecting a wallet.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bevanding/skills/antalpha-airdrop-hunter)
- [Repository](https://github.com/AntalphaAI/airdrop-hunter)
- [MCP repository](https://github.com/antalpha-com/antalpha-skills)
- [Grading system](references/grading-system.md)
- [Scam detection guide](references/scam-detection.md)
- [Output template](references/output-template.md)
- [Evaluation criteria](references/evaluation-criteria.md)
- [Trusted sources](references/trusted-sources.md)
- [Daily report template](assets/daily-report-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Structured Markdown reports with tables, warnings, and next-step options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include project grades, scam warnings, source links, and security disclaimers.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
