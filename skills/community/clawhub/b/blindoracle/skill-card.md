## Description:

Checks agent counterparties before payment by retrieving reputation, pre-hire, receipt, and delegation evidence from BlindOracle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craigmbrown](https://clawhub.ai/user/craigmbrown)

### License/Terms of Use:

Apache 2.0

## Use Case:

External developers and operators use BlindOracle to assess a counterparty agent before paying it, verify receipts, and record delegated work. The returned reputation and risk evidence does not guarantee identity or future performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A reputation lookup may send the subject being checked to api.craigmbrown.com.

Mitigation: Check whether the lookup is appropriate before sending a subject, and avoid sending information you are not comfortable sharing with the service.

Risk: Paid calls use x402 micropayments in USDC on Base and may settle irreversibly.

Mitigation: Check the live price in GET /v1/services and obtain operator approval before the first paid call and before any call priced at $1.00 or more.

Risk: A reputation score or sanctions no_match can be mistaken for proof of identity or safety.

Mitigation: Treat results as one source of evidence; do not treat a no_match as clearance or a score as a guarantee.

## Reference(s):

- [BlindOracle counterparty risk documentation](https://craigmbrown.com/blindoracle/counterparty-risk.html)
- [BlindOracle service catalog and live prices](https://api.craigmbrown.com/v1/services)
- [BlindOracle delegation chain verifier example](https://github.com/craigmbrown/blindoracle-sdk/blob/main/examples/verify_chain.py)
- [BlindOracle DID document](https://craigmbrown.com/.well-known/did.json)

## Skill Output:

**Output Type(s):** [API response data, Analysis, Guidance]

**Output Format:** [Structured service responses summarized as text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results are evidence for human decision-making, not a guarantee of trustworthiness.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
