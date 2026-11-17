## Description:

Queries JisuAPI with mobile carrier base-station identifiers to return approximate latitude, longitude, address, and accuracy details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jisuapi](https://clawhub.ai/user/jisuapi)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to answer explicit base-station lookup requests by turning MNC, LAC, and cell ID values into approximate location details from JisuAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Base-station identifiers can be location-sensitive, and lookups send those identifiers plus the configured API key to JisuAPI.

Mitigation: Use the skill only for explicit authorized requests, avoid querying another person's location-related data without proper authorization, and confirm users understand the lookup uses JisuAPI.

Risk: Returned coordinates and addresses are approximate and depend on upstream JisuAPI coverage.

Mitigation: Present results as approximate and avoid using them as sole evidence for safety-critical, legal, or emergency decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jisuapi/skills/cell)
- [JisuAPI Cell Query Documentation](https://www.jisuapi.com/api/cell/)
- [JisuAPI](https://www.jisuapi.com/)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jisuapi)

## Skill Output:

**Output Type(s):** [json, shell commands, configuration, guidance]

**Output Format:** [JSON result data plus human-facing setup and invocation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JISU_API_KEY and base-station identifiers; returns approximate location data when the upstream API has a match.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
