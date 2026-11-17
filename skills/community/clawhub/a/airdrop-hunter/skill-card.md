## Description:

Airdrop Hunter helps agents find, grade, and verify Web3 airdrop opportunities with S/A/B/C scoring, scam checks, daily reports, and zero-cost workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT

## Use Case:

External Web3 users and agents use this skill to scan airdrop opportunities, assess project quality, verify suspicious links before wallet interactions, and find zero-cost participation paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External URL checks and MCP tool calls may send airdrop URLs and project names to Antalpha's MCP service.

Mitigation: Use the skill only when that data sharing is acceptable, and strip private, signed, reset, invite, or token-bearing query strings and fragments before checking links.

Risk: The skill under-discloses persistent MCP credentials.

Mitigation: Store MCP agent identifiers and API keys in a secure secret store and avoid committing or pasting them into shared logs.

Risk: Airdrop grades and scam-check results are advisory and may be stale or incomplete.

Mitigation: Independently verify official domains and project channels before connecting a wallet, signing transactions, or acting on an opportunity.

## Reference(s):

- [Airdrop Hunter Skill Page](https://clawhub.ai/deanpeng-dotcom/skills/airdrop-hunter)
- [Airdrop Hunter Repository](https://github.com/AntalphaAI/airdrop-hunter)
- [Antalpha MCP Skills Repository](https://github.com/antalpha-com/antalpha-skills)
- [Antalpha MCP Endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Grading System](references/grading-system.md)
- [Scam Detection Guide](references/scam-detection.md)
- [Output Template](references/output-template.md)
- [Trusted Sources](references/trusted-sources.md)
- [Evaluation Criteria](references/evaluation-criteria.md)
- [Daily Report Template](assets/daily-report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown reports and tables rendered from MCP JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes S/A/B/C grades, scam-risk warnings, next-step options, and non-financial-advice disclaimers.]

## Skill Version(s):

1.3.1 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
