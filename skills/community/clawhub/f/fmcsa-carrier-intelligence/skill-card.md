## Description:

Vet a US interstate motor carrier by USDOT number before tendering freight: operating authority, insurance filings, out-of-service orders, safety history, and identity-linkage signals that help spot double brokering or a carrier re-registering under a new number. Free tools to try first; paid calls start at $0.01, are paid in USDC on Solana, Base or Polygon via x402, and are charged only when records are returned.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmcto](https://clawhub.ai/user/kmcto)

### License/Terms of Use:

MIT-0

## Use Case:

Freight brokers and carrier onboarding or risk teams use this skill to review US motor carrier authority, safety history, identity signals, and related records before tendering freight or evaluating an applicant.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious because caller-provided names and street addresses may be sent to an external service without a privacy warning or authorization.

Mitigation: Before submitting names or street addresses, review which fields will be sent and who receives them; avoid unrelated personal information unless the transfer has been reviewed and accepted.

## Reference(s):

- [FMCSA Carrier Intelligence for Agents](https://carriers.4sakeco.com/for-agents/)
- [Carrier Intelligence Service](https://carriers.4sakeco.com/)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance]

**Output Format:** [Structured carrier records with concise text or Markdown summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Carrier assessments are based on the available records and may include freshness and confidence caveats.]

## Skill Version(s):

1.3.1 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
