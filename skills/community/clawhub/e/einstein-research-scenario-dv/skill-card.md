## Description:

Analyzes news headlines into Japanese 18-month investment scenario reports with primary analysis, critical review, sector impact mapping, and stock recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdiri-ai](https://clawhub.ai/user/clawdiri-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn manually supplied market-moving headlines into Japanese 18-month scenario analysis. The report supports investment research by summarizing first-, second-, and third-order effects, sector sensitivity, stock recommendations, and a reviewer critique.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated stock recommendations may be over-trusted as financial advice.

Mitigation: Treat outputs as research support only, verify recommendations independently, and require human review before investment decisions.

Risk: Prompt-like headline text may manipulate or distort background-agent analysis.

Mitigation: Use clean headline inputs, avoid confidential or non-public information, and review assumptions before relying on the report.

Risk: Weakly scoped background-agent analysis can produce unsupported or stale market conclusions.

Mitigation: Validate key claims against current market data and preserve the reviewer critique as a required part of the final report.

## Reference(s):

- [Headline Event Patterns](references/headline_event_patterns.md)
- [Scenario Playbooks](references/scenario_playbooks.md)
- [Sector Sensitivity Matrix](references/sector_sensitivity_matrix.md)
- [ClawHub Skill Listing](https://clawhub.ai/clawdiri-ai/skills/einstein-research-scenario-dv)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Japanese Markdown report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes an 18-month scenario horizon, sector impact mapping, specific stock recommendations, and second-opinion review; does not execute trades.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
