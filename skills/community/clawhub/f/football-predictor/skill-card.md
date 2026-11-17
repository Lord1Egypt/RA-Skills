## Description:

Football Predictor collects match, odds, team, and weather signals to generate football match predictions, betting-oriented recommendations, result tracking, and learning updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warrenop](https://clawhub.ai/user/warrenop)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this agent to request football match analysis, daily recommendations, prediction statistics, and learning updates for sports analytics workflows. Recommendations are betting-oriented and should be reviewed before any real-world use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad agent permissions may let the skill perform actions beyond simple match analysis.

Mitigation: Review and narrow tool permissions before deployment, and run the skill in a sandbox until permissions are constrained.

Risk: Random mock data is used for betting-oriented recommendations, which can make outputs look more evidence-based than they are.

Mitigation: Clearly label or disable mock betting data and do not rely on recommendations as real betting advice in the current package.

Risk: EvoMap sharing and credential behavior are under-disclosed.

Mitigation: Document and gate EvoMap sharing, require approved HTTPS hub URLs, and avoid providing EvoMap secrets until those controls are in place.

Risk: Stored prediction history may contain user or workflow-sensitive records.

Mitigation: Add controls for prediction history retention, access, and deletion before production use.

## Reference(s):

- [Football Predictor data sources reference](references/data-sources.md)
- [ClawHub skill page](https://clawhub.ai/warrenop/skills/football-predictor)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON prediction and statistics objects with concise text recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include match names, prediction direction, confidence, odds, recommendation text, risk score, factors, statistics, and learning updates.]

## Skill Version(s):

1.0.0 (source: release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
