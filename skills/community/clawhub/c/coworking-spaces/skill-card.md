## Description:

Find nearby coworking spaces when the user asks for shared offices near them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users ask an agent to find coworking or shared office spaces near an authorized location, with optional radius, result limit, and amenity filters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on user location data to find nearby coworking spaces.

Mitigation: Use it only after the user intentionally requests nearby coworking results and authorizes location access.

Risk: Precise coordinates can expose sensitive location information if retained unnecessarily.

Mitigation: Avoid retaining exact coordinates and use coarse or grid-obfuscated location data when persistence is necessary.

Risk: Nearby-place results can be unavailable, rate limited, or constrained by invalid location or radius inputs.

Mitigation: Validate location and radius inputs and return the documented error states when data providers are unavailable or rate limits apply.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/coworking-spaces)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text describing standardized nearby coworking-space results and error states.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses authorized location, radius, limit, and optional filters; category is fixed to coworking-spaces.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
