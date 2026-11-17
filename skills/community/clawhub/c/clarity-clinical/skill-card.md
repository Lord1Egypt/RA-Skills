## Description:

Query clinical variant data from ClinVar and gnomAD via Clarity Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

Developers, researchers, and clinical data analysts use this skill to look up clinical significance, ClinVar review status, and gnomAD population frequency for genes or HGVS variants.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling can expose CLARITY_API_KEY on redirects.

Mitigation: Use the skill only after reviewing API-key behavior; prefer a hardened version that disables redirects or validates redirect targets before sending the key.

Risk: Clinical, patient-adjacent, or proprietary variant queries may expose sensitive information to an external API.

Mitigation: Submit only non-sensitive gene or variant queries unless authorized and aligned with applicable data-sharing requirements.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Protocol API](https://clarityprotocol.io/api/v1)
- [Clarity Clinical on ClawHub](https://clawhub.ai/clarityprotocol/skills/clarity-clinical)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [JSON or readable text summaries, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires internet access to clarityprotocol.io; optional CLARITY_API_KEY increases rate limits from 10 to 100 requests per minute.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
