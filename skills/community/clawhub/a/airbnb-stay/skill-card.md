## Description: <br>
Looks up one Airbnb listing through StayingAPI.com by listing ID, Airbnb room URL, or street address, returning details such as photos, reviews, host, amenities, availability, pricing, location, and rating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nikhonit](https://clawhub.ai/user/nikhonit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill when they already have a specific Airbnb listing ID, Airbnb room URL, or street address and need single-listing details rather than a search workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends listing identifiers, Airbnb URLs, or street addresses to the third-party Staying API service. <br>
Mitigation: Install only if Staying API is acceptable for the user's environment; use a scoped STAYINGAPI_KEY and prefer listing IDs or Airbnb URLs over private street addresses when possible. <br>
Risk: Address-based lookups consume more credits than listing ID or URL lookups. <br>
Mitigation: Prefer listing IDs or Airbnb room URLs when available and reserve street-address lookups for cases where no cheaper identifier exists. <br>


## Reference(s): <br>
- [Staying API](https://stayingapi.com) <br>
- [Staying API OpenAPI specification](https://stayingapi.com/openapi.json) <br>
- [Staying API MCP server](https://api.stayingapi.com/mcp) <br>
- [Staying API quickstart](https://stayingapi.com/quickstart/) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Python dict / JSON-like API response or error object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires STAYINGAPI_KEY; address lookups use more credits than listing ID or URL lookups.] <br>

## Skill Version(s): <br>
1.0.1 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
