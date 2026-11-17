## Description:

Routes and classifies personal finance questions so agents provide educational responses, disclose risks, avoid unsupported claims, minimize private financial data, and refer high-impact issues to qualified professionals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mindbomber](https://clawhub.ai/user/mindbomber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to handle investment, tax, budgeting, debt, credit, insurance, retirement, purchase, and other personal-finance conversations with clearer boundaries between general education and personalized advice. It helps route high-impact or unsupported financial claims toward trusted evidence, human review, or qualified professional guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may mistake cautious financial routing guidance for licensed financial, tax, legal, or investment advice.

Mitigation: Present outputs as general education or safety review guidance and route personalized, high-impact, tax, legal, investment, debt-crisis, or insurance decisions to qualified professionals.

Risk: Financial prompts may contain private account, tax, identity, credit, or purchase information.

Mitigation: Use minimal redacted summaries for review payloads and avoid including raw records, credentials, full payment numbers, bank details, tax IDs, credit reports, pay stubs, identity documents, or unrelated financial data.

Risk: The skill may add caution or referral language broadly because it is designed as a policy-style helper.

Mitigation: Apply it to finance-sensitive conversations and keep low-risk educational answers concise while preserving uncertainty, evidence, and risk caveats where relevant.

## Reference(s):

- [AANA Financial Safety Router Skill on ClawHub](https://clawhub.ai/mindbomber/skills/aana-financial-safety-router)
- [Review Payload Schema](schemas/financial-safety-review.schema.json)
- [Redacted Review Payload Example](examples/redacted-financial-safety-review.json)

## Skill Output:

**Output Type(s):** [guidance, markdown, JSON]

**Output Format:** [Markdown guidance with an optional structured JSON review payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Instruction-only; does not install dependencies, run commands, call services, persist memory, or inspect accounts by itself.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
