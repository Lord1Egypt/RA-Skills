## Description:

Look up FacilityBot records, summarize maintenance requests, and review facility operations through a connected read-only FacilityBot MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[trunnee0165](https://clawhub.ai/user/trunnee0165)

### License/Terms of Use:

MIT

## Use Case:

FacilityBot account users use the skill to review existing maintenance requests, assets, facilities, and related operational records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retrieved records can include personal information.

Mitigation: Connect only the intended FacilityBot account and grant read-only permissions appropriate to the records needed.

Risk: The external MCP service and its enforcement of permissions were outside the artifact review.

Mitigation: Confirm the connection's permissions and use it only to access records the account is authorized to view.

## Reference(s):

- [FacilityBot read-only API capabilities](references/api-capabilities.md)
- [FacilityBot Public API documentation](https://portal.facilitybot.co/client-api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Natural-language summaries and guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.0.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
