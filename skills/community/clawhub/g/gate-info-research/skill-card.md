## Description:

Produces structured, citation-backed crypto market research reports for market overviews, coin analysis, coin comparisons, technical trends, event attribution, and token risk checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to understand crypto markets, compare coins, review technical and news signals, and assess token risks before making their own decisions. It is for data-driven research only and does not place trades, move funds, or provide investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill refers to mutable remote runtime rules and says they have highest priority.

Mitigation: Review the referenced runtime rules before installation and prefer a vendored or pinned version controlled with the release.

Risk: The workflow may ask for a session credential if authentication is required.

Mitigation: Do not paste session tokens, cookies, API keys, or account credentials into chat; use only approved authentication channels.

Risk: Crypto market data can be stale, incomplete, or conflicting across data dimensions.

Mitigation: Treat outputs as research, verify important facts against current market sources, and do not rely on the report as investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gate-exchange/skills/gate-info-research)
- [Gate Research Copilot MCP Specification](references/mcp.md)
- [Scenarios and Prompt Examples](references/scenarios.md)
- [Gate runtime rules](https://github.com/gate/gate-skills/blob/master/skills/gate-runtime-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research reports with citations, timestamps, missing-data notes, and a non-investment-advice disclaimer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include market summaries, comparison tables, technical summaries, event attribution, risk checks, and explicit data-gap annotations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2026.3.23-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
