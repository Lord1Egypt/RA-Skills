## Description:

Analyzes Chinese A-share capital flows, including main-force net inflows, northbound holdings, and trading leaderboard signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gbabyzs](https://clawhub.ai/user/gbabyzs)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis agents use this skill to retrieve and summarize Chinese A-share capital-flow signals for stock research workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches third-party financial data through akshare, which may be unsuitable for some environments or workflows.

Mitigation: Install only where third-party financial data access is acceptable and verify returned signals before use.

Risk: Dependency behavior can change across akshare or pandas releases.

Mitigation: Pin dependency versions before production use.

Risk: Documentation and returned field names are Chinese-market specific and may be misunderstood outside that context.

Mitigation: Confirm the Chinese documentation and financial signal meanings match the intended analysis workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gbabyzs/skills/capital-flow-analysis)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Artifact Skill Manifest](artifact/skill.json)

## Skill Output:

**Output Type(s):** [Text, Code, Guidance]

**Output Format:** [Markdown and Python dictionary outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses akshare and pandas to fetch third-party financial data when called.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
