## Description:

Queries CENC earthquake catalog data for selected times and regions, filters by magnitude, and returns earthquake time, location, magnitude, depth, and coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangpeng258](https://clawhub.ai/user/wangpeng258)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer questions about recent or historical earthquakes in China or globally. It queries CENC data and helps summarize records by time, place, magnitude, and depth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts CENC when earthquake information is requested.

Mitigation: Install and use it only where outbound access to CENC is acceptable, and review network behavior before deployment.

Risk: Invocation rules are broad for earthquake-related questions.

Mitigation: Review agent routing so the skill is invoked only for earthquake information queries that require CENC data.

## Reference(s):

- [CENC earthquake catalog endpoint](https://www.cenc.ac.cn/prodlaunch-web-backend/open/data/catalogs)
- [ClawHub skill page](https://clawhub.ai/wangpeng258/skills/earthquake-info-query)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON, Guidance]

**Output Format:** [JSON result object plus natural-language summary guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success responses with count and earthquake records, or error responses for parameter and request failures.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
