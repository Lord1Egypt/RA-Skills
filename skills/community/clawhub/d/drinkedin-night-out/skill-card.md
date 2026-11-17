## Description:

Plans walkable bar crawls and nights out for adults of legal drinking age using DrinkedIn-validated venues through the free Night Out MCP server; it refuses venue planning for underage users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haim-barad](https://clawhub.ai/user/haim-barad)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request a walkable route for a bar crawl, date night, or other night out near a place they choose. The skill uses DrinkedIn-validated venues and does not plan venue visits for people under the legal drinking age.

### Deployment Geography for Use:

Global; venue coverage is limited to places with validated records.

## Known Risks and Mitigations:

Risk: The security review is partial because some Markdown references could not be resolved.

Mitigation: Review the unresolved references before relying on the skill; the reviewed content had no reported security findings.

Risk: A typed address is sent to the public OpenStreetMap Nominatim geocoder.

Mitigation: Prefer user-provided coordinates or a named area when suitable, and explain the geocoding if the user asks where the address goes.

Risk: Anyone with a route share link can view it while the saved route is retained for 30 days after its last planning.

Mitigation: Offer the link only when the user wants to share or save the route, and clarify that anyone holding it can open it.

## Reference(s):

- [DrinkedIn Night Out documentation](https://drinkedin.net/docs/night-out)
- [DrinkedIn Night Out MCP server](https://ai.drinkedin.net/mcp/night-out)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown route plan with venue details, walking estimates, links, and user guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes contain 2–4 stops and use validated venue data. Hours and prices are unverified, and walking times are estimates.]

## Skill Version(s):

1.5.1 (source: release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
