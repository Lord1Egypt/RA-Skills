## Description:

Freshness Judge labels normalized evidence against a canonical time window as current, background, stale, undated, or malformed and produces a freshness profile for downstream use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill after evidence normalization to separate current evidence from background, stale, undated, or malformed material for news, policy, market analysis, and other time-sensitive tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested compensation_queries could trigger unnecessary or biased follow-up searches if treated as automatic actions.

Mitigation: Treat compensation_queries as recommendations and require orchestrator or user approval unless automatic follow-up search is intentionally enabled.

Risk: Chinese-only documentation may be unsuitable for users who need English or multilingual operating instructions.

Mitigation: Confirm language fit before deployment or provide reviewed translated documentation for the target user group.

Risk: Undated or boundary evidence can make older material appear more current than it is when downstream systems ignore freshness labels.

Mitigation: Preserve the freshness buckets and review freshness_profile risk_flags before using outputs in final analysis or decisions.

## Reference(s):

- [Freshness Judge on ClawHub](https://clawhub.ai/z1one0415/skills/freshness-judge)
- [Freshness Rules](references/freshness-rules.md)
- [Time Window Examples](references/time-window-examples.md)
- [Judgment Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [JSON object with freshness buckets, a freshness_profile, risk_flags, and optional compensation_queries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Retains stale and undated evidence in categorized outputs; compensation_queries should be treated as recommendations unless automatic follow-up search is intentionally enabled.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
