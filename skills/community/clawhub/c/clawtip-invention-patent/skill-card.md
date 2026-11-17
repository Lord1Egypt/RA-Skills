## Description:

Chinese invention patent application drafting assistant that requires a successful 2.00 RMB payment before guiding the user through Chinese-language drafts for the specification, claims, abstract, and related patent sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liliangwen-spec](https://clawhub.ai/user/liliangwen-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create a paid drafting session for Chinese invention patent application materials, then receive step-by-step Chinese guidance and draft text after payment verification. Outputs are drafts for later review and refinement by the applicant or a patent professional.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Patent topics, order numbers, and payment credentials are sent to a publisher-operated remote service over plaintext HTTP.

Mitigation: Install only after accepting that exposure; avoid trade-secret-level or pre-filing confidential material unless the service moves to HTTPS and provides clear privacy, retention, and payment-security terms.

Risk: The skill produces patent application drafts rather than legal advice or submission-ready filings.

Mitigation: Have the applicant or a qualified patent professional review and revise the drafts against the applicable patent-office requirements before filing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Chinese Markdown with command snippets and structured patent draft sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires successful order creation, payment handling through clawtip, and fulfillment verification before patent drafting begins.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
