## Description:

Intelligent search for agents. Multi-source retrieval with confidence scoring - web, academic, and Tavily in one unified API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aisapay](https://clawhub.ai/user/aisapay)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to run web, academic, smart, full-text, and Tavily-backed searches through the AISA API, then reason over retrieved results with confidence scoring and synthesis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, supplied URLs, retrieved result payloads, and the AISA API key are sent to an external AISA service and Tavily-backed endpoints.

Mitigation: Avoid confidential queries, protect the API key, and review provider data handling before use.

Risk: Extract, crawl, and map operations can send private, internal, authenticated, signed, or token-bearing URLs to external services.

Mitigation: Use these operations only on URLs you are authorized to process and avoid internal or credential-bearing links unless explicitly approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aisapay/skills/aisa-multi-source-search)
- [OpenClaw Homepage](https://openclaw.ai)
- [AIsa API Documentation](https://aisa.mintlify.app)
- [AIsa API Reference](https://aisa.mintlify.app/api-reference/introduction)
- [AIsa Verity Reference Implementation](https://github.com/AIsa-team/verity)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, Python examples, and JSON API responses.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires AISA_API_KEY and sends user-directed queries, URLs, and result payloads to external AISA and Tavily-backed endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
