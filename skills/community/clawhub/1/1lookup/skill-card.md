## Description:

Validate and enrich phone numbers, email addresses and IP addresses with the 1Lookup API. Phone validation, line type and carrier, HLR live network status, reverse phone (caller name), spam reputation, email deliverability and IP geolocation with proxy checks. Use when the user asks whether a number, email or IP is real, what kind of line it is, who owns it, or whether it is safe to contact.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robbyfrank](https://clawhub.ai/user/robbyfrank)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to validate phone numbers, email addresses and IP addresses, check carrier and spam signals, and retrieve requested phone or network details through 1Lookup. It helps agents answer whether contact information appears valid or carries indicators relevant to contacting it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary notes that identifiers are sent to 1Lookup, flags an account retrieval action as a possible purpose mismatch, and says the scan was partial; it also notes a missing privacy notice.

Mitigation: Use lookups only for identifiers the user asked to check, make sure the user expects those identifiers to be sent to 1Lookup, review account retrieval against the requested task, and treat the security assessment as incomplete.

## Reference(s):

- [1Lookup website](https://www.1lookup.io)
- [1Lookup API documentation](https://app.1lookup.io/api)
- [1Lookup OpenAPI description](https://www.1lookup.io/openapi.json)
- [1Lookup pricing](https://www.1lookup.io/pricing)
- [1Lookup MCP server card](https://www.1lookup.io/.well-known/mcp/server-card.json)
- [1Lookup API key dashboard](https://app.1lookup.io/api-keys)
- [1Lookup skill release](https://clawhub.ai/robbyfrank/skills/1lookup)

## Skill Output:

**Output Type(s):** [Text, Analysis, API Calls, Shell commands, Configuration instructions]

**Output Format:** [Text or Markdown lookup summaries, with JSON API response examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results may contain personal or sensitive identifiers; API calls can spend account credits.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
