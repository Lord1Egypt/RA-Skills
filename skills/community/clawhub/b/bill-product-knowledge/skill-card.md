## Description:

Answers questions about bill products, discounting, financing, signing, quotas, quotes, contracts, invoices, and related platform operations from the bundled bill_knowledge Markdown knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krillingone](https://clawhub.ai/user/krillingone)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and support agents use this skill to answer Chinese bill-product questions and summarize platform operation steps from local Markdown documentation. It is intended for knowledge-base retrieval, not investment advice, legal advice, compliance conclusions, or financial decision-making.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can repeat financial login, KYC, tax, SMS verification, biometric, invoice, contract, and payment instructions.

Mitigation: Configure the agent to remind users not to paste passwords, SMS codes, tax credentials, ID scans, contracts, invoices, or bank details into chat; users should enter sensitive data only on independently verified official HTTPS sites or official apps.

Risk: Some source guidance includes plaintext HTTP disclosure-platform links and a mandatory promotional footer.

Mitigation: Review the footer for deployment suitability and replace plaintext HTTP disclosure-platform links with verified HTTPS destinations before relying on the guidance.

Risk: Financial product answers may be mistaken for investment, legal, or compliance advice.

Mitigation: Keep responses limited to the local knowledge base, cite source filenames, and avoid investment recommendations, legal conclusions, or compliance commitments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/krillingone/skills/bill-product-knowledge)
- [重庆富民银行富票融平台](https://p.fbank.com/home/ticket)
- [富票融平台登录入口](https://p.fbank.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Markdown answers with cited source filenames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses should be grounded in matched bill_knowledge Markdown files and should state when the local knowledge base does not cover the question.]

## Skill Version(s):

1.0.12 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
