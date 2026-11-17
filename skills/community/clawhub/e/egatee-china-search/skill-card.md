## Description:

Calls Egatee Web2JDE Orchestrator text and image product search APIs, returns product card data for agents, and supports optional RFQ candidate capture with MySQL-backed search supplementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahoyoshi](https://clawhub.ai/user/ahoyoshi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to connect chat workflows to Egatee product search, present text or image search results as product cards, and prepare RFQ candidate data after the agent confirms user intent and contact details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext HTTP or untrusted endpoint configuration may expose search traffic or credentials.

Mitigation: Use trusted HTTPS endpoints for production, restrict environment overrides, and review endpoint configuration before deployment.

Risk: Arbitrary image URLs can create SSRF, content-size, or unsafe fetch risks.

Mitigation: Allow only trusted image sources or add SSRF, redirect, scheme, IP range, timeout, and size controls before accepting untrusted image URLs.

Risk: API keys or bearer tokens passed through chat payloads may be retained in logs or conversation state.

Mitigation: Prefer managed secret injection or environment variables and avoid placing bearer tokens directly in user-visible chat payloads.

Risk: RFQ capture can involve phone numbers and other contact details.

Mitigation: Gate RFQ saving on explicit user consent and add redaction or data-handling review before enabling persistence.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ahoyoshi/skills/egatee-china-search)
- [Publisher profile](https://clawhub.ai/user/ahoyoshi)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses with product lists, card objects, Markdown and HTML card renderings, RFQ candidate data, and setup or CLI command guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include outbound API results, image URLs, local rate-limit status, and database-backed RFQ or SQL supplement metadata when configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
