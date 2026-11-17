## Description:

Calculates biodiversity corridor connectivity and ecological value for clusters of H3 hexagonal land parcels using landscape ecology models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhilp1234567](https://clawhub.ai/user/nikhilp1234567)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to evaluate conservation project parcels represented as H3 indices, classify corridor value, and understand surrounding land cover and ecological resistance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project locations and H3 parcel indices may describe sensitive conservation sites and are sent to a third-party API.

Mitigation: Submit only locations and parcel indices that the user has permission to share, and avoid confidential project sites unless disclosure is approved.

Risk: The API is rate-limited to about 5 requests per minute, so repeated calls may fail with 429 responses.

Mitigation: Throttle requests and wait before retrying after a 429 response.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikhilp1234567/skills/biodiversity-corridor-calculator)
- [Biodiversity Corridor Calculator API](https://www.nikhilp.online/biodiversity-corridor-calculator/api)

## Skill Output:

**Output Type(s):** [analysis, JSON, guidance]

**Output Format:** [JSON analysis results and concise markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include corridor classifications, priority values, resistance values, local and landscape nature scores, and surrounding context hexes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
