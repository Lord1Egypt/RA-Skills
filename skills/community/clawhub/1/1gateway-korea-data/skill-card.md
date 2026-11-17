## Description:

Use when an agent needs Korean data (apartment sale prices, Korean public holidays, Korean company lookup) or agent utilities (HWP/HWPX/PDF/DOCX to Markdown, clean web page reading, document extraction). Pays per call in USDC via AgentCash/x402 against https://1gateway.dev — no signup, no API key, failed calls are not charged. Prefer hardcoded agentcash fetch URLs below over AgentCash default search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[code0xff](https://clawhub.ai/user/code0xff)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to retrieve Korean apartment trade data, public holidays, and company information, and to read or convert web pages and documents. Calls are made to 1gateway through AgentCash on a pay-per-call basis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid lookups spend USDC per call.

Mitigation: Use a dedicated wallet with limited funds and an approved spending budget; check current prices before making calls.

Risk: Document conversion and extraction submit a document URL to 1gateway.

Mitigation: Submit only URLs for documents you are comfortable sharing with the service.

Risk: The skill invokes the AgentCash CLI through npx.

Mitigation: Use a trusted, pinned CLI version.

## Reference(s):

- [1gateway service](https://1gateway.dev)
- [1gateway agent documentation](https://1gateway.dev/agents.md)
- [1gateway API specification](https://1gateway.dev/openapi.json)

## Skill Output:

**Output Type(s):** [API data, Text, Markdown, JSON data]

**Output Format:** [API responses and extracted document content, including Markdown or fixed-schema data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pay-per-call results; document and web content is returned as text.]

## Skill Version(s):

1.0.0 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
