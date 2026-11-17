## Description:

Submit research questions for AI-powered analysis via Clarity Protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

External developers and research teams use this skill to submit protein variant or mutation research questions to Clarity Protocol and receive AI-generated analysis grounded in aggregated biomedical sources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research questions, variant identifiers, focus terms, and optional context are sent to Clarity Protocol's remote service.

Mitigation: Do not submit secrets, regulated health data, or proprietary research unless Clarity Protocol is approved for that data.

Risk: The skill requires a write API key for remote analysis requests.

Mitigation: Store the key in CLARITY_WRITE_API_KEY, restrict access to the environment, and rotate the key if exposure is suspected.

## Reference(s):

- [Clarity Protocol Homepage](https://clarityprotocol.io)
- [Clarity Protocol API Base](https://clarityprotocol.io/api/v1)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [JSON, plain text, or terminal summary from a remote analysis response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLARITY_WRITE_API_KEY, sends questions and optional context to Clarity Protocol, and is limited to 10 analysis requests per API key per day.]

## Skill Version(s):

1.0.0 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
