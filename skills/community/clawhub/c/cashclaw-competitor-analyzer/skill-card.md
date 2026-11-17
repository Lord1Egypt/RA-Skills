## Description:

Performs competitor research and generates detailed analysis reports with market positioning insights, including feature comparison, pricing analysis, SWOT analysis, and strategic recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[andreataide86](https://clawhub.ai/user/andreataide86)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business analysts use this skill to research competitors and produce paid competitive-analysis deliverables grounded in observable public data. It is intended for feature, pricing, positioning, SWOT, and recommendation reports comparing a client's product against identified competitors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the current npm cashclaw package, which is not pinned by the artifact evidence.

Mitigation: Review the installed package version and run it only in environments where use of the current cashclaw CLI is acceptable.

Risk: Generated reports may aggregate third-party business data and include a CashClaw attribution footer.

Mitigation: Review reports before storing or sharing them, and confirm that included business data and attribution are appropriate for the audience.

Risk: Competitor pricing, review counts, funding, and positioning data can become stale or be unavailable from public sources.

Mitigation: Verify source data close to delivery time, label unavailable data clearly, and avoid presenting assumptions as facts.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/andreataide86/skills/cashclaw-competitor-analyzer)
- [Publisher profile](https://clawhub.ai/user/andreataide86)
- [CashClaw npm package](https://www.npmjs.com/package/cashclaw)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown reports, JSON comparison matrices, and inline shell commands for the CashClaw CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include source-backed findings, methodology notes, and a CashClaw attribution footer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
