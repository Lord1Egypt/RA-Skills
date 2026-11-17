## Description:

Analyzes retail chain expansion opportunities, candidate-address competition, and rollout order from Tencent Map address text and DDT published retail store snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[horacetu](https://clawhub.ai/user/horacetu)

### License/Terms of Use:

MIT-0

## Use Case:

Retail expansion, operations, and real-estate teams use this skill to evaluate published retail brands, opportunity cities, local competitive density, and candidate-site screening questions from Tencent Map address text. It helps narrow decisions to verifiable candidate locations using DDT's current published store snapshot.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A bearer API key could be sent to an inherited or untrusted custom API endpoint.

Mitigation: Set DDT_OPEN_BASE explicitly to the trusted DDT API host or clear inherited values before use; use a scoped, revocable DDT_API_KEY.

Risk: Brand names, addresses, and coordinates submitted for analysis are sent to the DDT API.

Mitigation: Use the skill only in a controlled environment and avoid submitting sensitive or confidential location plans unless the API use is approved.

Risk: Site-screening output is based on published snapshots and limited previews, so it can be mistaken for a complete market list or success forecast.

Mitigation: Treat results as initial screening guidance, check coverage and truncation flags, and require field verification before business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/horacetu/skills/ddt-tencent-map-retail-expansion)
- [DDT Claw homepage](https://gotoshop-ai.com/ddtclaw/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown retail site-selection analysis with concise metrics, coverage notes, and optional shell commands for API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should avoid API keys, internal identifiers, supplier fields, and unsupported metrics; limited store previews are shown only when the user asks for specific stores or candidate points.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
