## Description:

Discover specialist Airnode Hub APIs and verify responses against the selected signer and exact request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daav3](https://clawhub.ai/user/daav3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Airnode Hub API listings, select operations that fit a request, execute free calls or hand off paid calls, and verify Airnode attestations against the expected signer and exact request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Airnode Hub and catalogue-listed provider APIs during discovery, inspection, execution, and verification.

Mitigation: Install only where this disclosed network access is acceptable, and keep calls scoped to the live Hub catalogue and selected provider endpoints.

Risk: Paid operations may require separate payment authorization and could create spend exposure if handled outside the skill boundary.

Mitigation: Do not provide private keys or payment secrets to the skill; route paid operations through a separate authorized payer with explicit spend limits, timeout policy, and retained settlement evidence.

Risk: A valid Airnode attestation proves signer and request binding, not upstream factual accuracy, completeness, or source freshness.

Mitigation: Report signing time, source observation time when available, provider errors, pagination boundaries, missing coverage, and stale or unknown timestamps.

Risk: Incorrect operation selection, parameters, signer expectations, or responseProjection can produce misleading results or failed verification.

Mitigation: Validate the live Airnode document against the listing, preserve exact parameters and projection, investigate signer mismatches, and present unresolved failures instead of treating verification failures as successful answers.

## Reference(s):

- [Airnode Hub HTTP contract](references/http-contract.md)
- [Airnode Hub payment policy](references/payment-policy.md)
- [Airnode Hub MCP documentation](https://airnodehub-docs.api3.org/api-consumers/mcp)
- [Airnode attestation documentation](https://airnodehub-docs.api3.org/airnode/attestation)
- [Airnode Hub catalogue](https://airnodehub.api3.org/llms.txt)
- [Airnode Hub full catalogue](https://airnodehub.api3.org/llms-full.txt)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include selected listing and operation details, exact parameters, responseProjection, signer identity, attestation details, source freshness notes, and unresolved failure states.]

## Skill Version(s):

0.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
