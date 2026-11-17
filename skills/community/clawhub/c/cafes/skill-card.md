## Description:

Find nearby cafes. Invoke when user asks for coffee near me.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikeclaw007](https://clawhub.ai/user/mikeclaw007)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill to find nearby cafes from an authorized location, with configurable radius, result limits, and filters such as chain status, rating, or seating.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires user location and could expose precise coordinates if location data is retained or reused unnecessarily.

Mitigation: Request location authorization before lookup and avoid retaining precise coordinates; use coarse grid handling where possible.

Risk: The referenced STANDARD_RESPONSE.md file is not included in the release, so exact response formatting may be ambiguous.

Mitigation: Confirm the expected POI response schema before integrating the skill into automated workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Markdown or structured POI list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include standardized cafe POI fields, provider/rate-limit error codes, and privacy guidance for location handling.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
