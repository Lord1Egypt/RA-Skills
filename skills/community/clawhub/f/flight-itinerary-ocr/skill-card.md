## Description:

Extracts passenger, identity, flight, route, time, fare, surcharge, civil aviation fund, and e-ticket number fields from Chinese air transport e-ticket itineraries using the Scnet OCR API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scnet-sugon](https://clawhub.ai/user/scnet-sugon)

### License/Terms of Use:

MIT

## Use Case:

Employees, external users, and developers use this skill to OCR flight itinerary images, PDFs, or supported archives and receive structured itinerary fields for downstream review or automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload sensitive local itinerary documents to an external OCR endpoint.

Mitigation: Use it only with files approved for Scnet or the configured OCR endpoint, and run it with access limited to the specific documents intended for OCR.

Risk: The configurable SCNET_API_BASE value can redirect documents and the bearer token to another endpoint.

Mitigation: Keep SCNET_API_BASE set to the documented HTTPS Scnet API unless the replacement endpoint is fully trusted.

Risk: The API key is read from the local environment or .env configuration.

Mitigation: Store SCNET_API_KEY carefully, avoid sharing it in chats or logs, and prefer an isolated runtime with restricted file permissions.

## Reference(s):

- [Sugon-Scnet OCR API documentation summary](references/api-docs.md)
- [OCR field summary](assets/templates/fields-summary.md)
- [Scnet website](https://www.scnet.cn)
- [Scnet OCR API endpoint](https://api.scnet.cn/api/llm/v1)
- [ClawHub skill page](https://clawhub.ai/scnet-sugon/skills/flight-itinerary-ocr)
- [Publisher profile](https://clawhub.ai/user/scnet-sugon)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Pretty-printed JSON on standard output, with localized plain-text error messages on failure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the Scnet OCR data array after removing confidence fields from result items.]

## Skill Version(s):

1.0.5 (source: frontmatter, skill.yaml, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
