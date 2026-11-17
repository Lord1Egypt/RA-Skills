## Description:

Reconciles company and brand identities across public domains, LinkedIn company profiles, SEC registrants, and employer records while preserving ambiguous or distinct relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Analysts and developers use this skill to deduplicate supplied company lists or a bounded discovery set, producing a reviewable identity crosswalk with source evidence, relationship distinctions, and unresolved conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company names, domains, URLs, lookup queries, and an API key are sent to Crawlora.

Mitigation: Use only records approved for this service, safeguard the API key, and bound requests to the intended scope.

Risk: Web, hiring-board, and cached observations may be stale or mistaken for proof of legal ownership or current business status.

Mitigation: Retain source and observation dates, corroborate relationships, and review the evidence ledger before acting on the mapping.

## Reference(s):

- [Company identity reconciliation release](https://clawhub.ai/crawlora-org/skills/company-identity-reconciliation)
- [Crawlora endpoint reference](artifact/reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown tables and evidence ledger]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scoped canonical records, alias and ID crosswalk, relationship decisions, source dates, conflicts, and missing lookups.]

## Skill Version(s):

1.0.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
