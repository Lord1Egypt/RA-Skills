## Description:

Provides agents with Argentine CUIT/CUIL and CBU/CVU validation, phone normalization, and current dollar exchange rates through a remote service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[torlettijoaquin](https://clawhub.ai/user/torlettijoaquin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use the service to validate Argentine tax and bank identifiers, normalize Argentine phone numbers, and retrieve dollar exchange rates. The service is accessed through MCP or REST and charges prepaid credits for successful calls.

### Deployment Geography for Use:

Argentina

## Known Risks and Mitigations:

Risk: Tax, bank, or phone identifiers are sent to a remote service.

Mitigation: Use the service only for lookups approved for external processing, and review its privacy practices before submitting identifiers.

Risk: API calls consume prepaid credits, and the API key grants access to the account.

Mitigation: Protect AR_TOOLS_API_KEY and check balance and pricing before running batches of lookups.

Risk: The live service and publisher identity could not be independently verified during this review.

Mitigation: Verify the service endpoint and publisher through trusted channels before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/torlettijoaquin/skills/ar-tools)
- [AR Tools service](https://ar-tools-api-103907796853.us-east1.run.app)
- [MCP endpoint](https://ar-tools-api-103907796853.us-east1.run.app/mcp)
- [REST OpenAPI specification](https://ar-tools-api-103907796853.us-east1.run.app/openapi.json)
- [Service usage guide](https://ar-tools-api-103907796853.us-east1.run.app/skill.md)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured lookup results that an agent can present as text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on remote service and external data providers; calls consume prepaid credits.]

## Skill Version(s):

0.1.1 (source: SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
