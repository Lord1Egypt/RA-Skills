## Description: <br>
Calculates biodiversity corridor connectivity and ecological value for clusters of H3 hexagonal land parcels using landscape ecology models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhilp1234567](https://clawhub.ai/user/nikhilp1234567) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and conservation-planning agents use this skill to evaluate H3-indexed land parcels for corridor, stepping-stone, or regeneration potential and to retrieve surrounding land-cover context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Exact center coordinates and H3 parcel indices are sent to a third-party API. <br>
Mitigation: Use public or synthetic locations first, avoid confidential conservation or property sites unless the service operator is trusted, and require approval before sending exact locations. <br>
Risk: The API is rate-limited to about 5 requests per minute. <br>
Mitigation: Wait before retrying after 429 responses and keep requests within the documented 50-hex limit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nikhilp1234567/biodiversity-corridor-calculator) <br>
- [Publisher profile](https://clawhub.ai/user/nikhilp1234567) <br>
- [Biodiversity Corridor Calculator API](https://www.nikhilp.online/biodiversity-corridor-calculator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Markdown instructions with JSON request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [API requests use center latitude, center longitude, and up to 50 resolution-9 H3 indices; callers should handle 429 rate-limit responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
