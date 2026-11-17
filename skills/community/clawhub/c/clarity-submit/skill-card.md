## Description:

Submit a protein variant hypothesis to Clarity Protocol for validation and folding, and check the status of submitted hypotheses.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarityprotocol](https://clawhub.ai/user/clarityprotocol)

### License/Terms of Use:

MIT

## Use Case:

Researchers, developers, and agent builders use this skill to submit protein variant hypotheses to Clarity Protocol for validation, structural prediction, and status tracking in research pipelines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submissions send protein, variant, rationale, optional disease, and optional wallet information to Clarity Protocol.

Mitigation: Use the skill only for explicit submission or status-check requests, and avoid submitting sensitive research details unless sharing them with Clarity Protocol is acceptable.

Risk: Write access depends on CLARITY_WRITE_KEY, which could enable unintended submissions if exposed.

Mitigation: Keep CLARITY_WRITE_KEY private, scope it where possible, and provide it only in environments intended for Clarity Protocol submissions.

Risk: The external service applies rate limits and may reject invalid inputs or proteins beyond supported size limits.

Mitigation: Review inputs before submission, handle authentication, validation, and rate-limit errors, and use returned hypothesis IDs for follow-up status checks.

## Reference(s):

- [Clarity Protocol](https://clarityprotocol.io)
- [Clarity Submit on ClawHub](https://clawhub.ai/clarityprotocol/skills/clarity-submit)
- [clarityprotocol Publisher Profile](https://clawhub.ai/user/clarityprotocol)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON status and submission results, often shown with shell command usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submissions require CLARITY_WRITE_KEY; status checks can return human-readable summaries or JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
