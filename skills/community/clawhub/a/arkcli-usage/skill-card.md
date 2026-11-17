## Description:

Helps agents use arkcli to inspect inference usage, subscription quotas, balances, and team-seat consumption while respecting each query's scope and freshness limits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jasonstarlight](https://clawhub.ai/user/jasonstarlight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to query ARK inference usage, plan quota snapshots, balances, Agent Plan model details, and team-seat usage. It helps them select the right usage view and explain its limits when reporting results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes a mismatch involving team-seat inventory examples and says one local reference was unavailable during scanning.

Mitigation: Review the team-seat examples against the usage-only scope and complete review of the missing reference before release.

Risk: Aggregated usage statistics may be delayed by 5–30 minutes, which can make them unsuitable for real-time budgets or alerts.

Mitigation: Use per-request usage data for real-time monitoring and reserve aggregated statistics for delayed analysis.

## Reference(s):

- [arkcli usage release page](https://clawhub.ai/jasonstarlight/skills/arkcli-usage)
- [arkcli-usage-stats.md](artifact/references/arkcli-usage-stats.md)
- [arkcli-usage-plan.md](artifact/references/arkcli-usage-plan.md)
- [arkcli-usage-plan-details.md](artifact/references/arkcli-usage-plan-details.md)
- [arkcli-usage-balance.md](artifact/references/arkcli-usage-balance.md)
- [arkcli-usage-seats.md](artifact/references/arkcli-usage-seats.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance, Shell commands, JSON]

**Output Format:** [Natural-language usage summaries and arkcli command guidance; CLI results are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Usage summaries may include aggregated statistics, quota snapshots, balances, and team-seat usage. Aggregated stats can be delayed by 5–30 minutes.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence; skill frontmatter reports 1.3.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
