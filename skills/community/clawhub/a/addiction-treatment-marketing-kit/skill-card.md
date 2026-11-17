## Description:

Generates marketing prompts and templates for licensed addiction treatment and behavioral health providers, including patient acquisition campaigns, paid and organic advertising content, website copy, JSON-LD schema, reputation responses, and outreach materials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitflopez](https://clawhub.ai/user/gitflopez)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare marketers, compliance officers, and licensed behavioral health providers use this skill to draft addiction treatment marketing assets and review them against stated compliance gates before publication. It is intended for U.S. behavioral health marketing workflows that require human legal, compliance, and credential review.

### Deployment Geography for Use:

United States, with Nevada-specific licensing and regulatory prompts

## Known Risks and Mitigations:

Risk: Generated content can include false or inapplicable certification, accreditation, license, payer-network, or clinical credential claims if placeholders, examples, or fixed footers are published without verification.

Mitigation: Verify active LegitScript status, facility licensing, accreditation, staff credentials, payer network status, MAT prescribing authority, and OTP status before publishing; remove or conditionally render any claim that is not active, verified, and applicable.

Risk: Healthcare marketing outputs may be treated as compliance-ready even though the server security review flagged risk in certification and credential claims.

Mitigation: Require human compliance and legal review before production use, and do not rely on the skill's compliance claims as the sole basis for publication or ad submission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gitflopez/skills/addiction-treatment-marketing-kit)
- [Publisher profile](https://clawhub.ai/user/gitflopez)
- [README](artifact/README.md)
- [Marketing notes](artifact/MARKETING.md)
- [Sample output](artifact/examples/sample-output.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown prompt outputs with optional JSON-LD code blocks, campaign copy, checklist text, and review guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only outputs require human legal, compliance, credential, and advertising-platform review before use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
