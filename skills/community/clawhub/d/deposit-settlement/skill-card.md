## Description:

Settle a US rental security deposit after move-out with the Tektolo deposit settlement engine - the return deadline, which deductions are allowed and how much after depreciation, interest owed, the refund, penalty exposure and a draft itemized statement, every rule cited. Use when a landlord or property manager is closing a move-out, when a tenant asks whether a deposit came back on time or a deduction is allowed, or for a state's deposit rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tektolo](https://clawhub.ai/user/tektolo)

### License/Terms of Use:

MIT-0

## Use Case:

External landlords, property managers, and tenants use the skill to assess a US rental security deposit after move-out, including return deadlines, deductions, interest, refunds, and potential statutory penalties. It can also summarize deposit rules for a state or a supported city.

### Deployment Geography for Use:

United States, with city-specific rules for the covered cities listed in the skill documentation.

## Known Risks and Mitigations:

Risk: Rental details sent to the settlement service may include personal or account information.

Mitigation: Submit only information needed for the calculation; omit names, addresses, account details, and unrelated personal information.

Risk: A calculated assessment or draft itemized statement may be incomplete or unsuitable for a particular situation.

Mitigation: Review the cited rules, warnings, assumptions, and draft before relying on it; the user makes the decision and signs and sends any statement.

## Reference(s):

- [Tektolo deposit settlement capability and schemas](https://tektolo.com/capabilities/deposit-settlement)
- [Tektolo rental-property MCP endpoint](https://tektolo.com/mcp/rental-property)
- [Tektolo deposit settlement REST endpoint](https://tektolo.com/v1/deposit-settlement/settle)
- [Tektolo catalog and schemas](https://tektolo.com/catalog.json)
- [ClawHub release](https://clawhub.ai/tektolo/skills/deposit-settlement)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown]

**Output Format:** [Structured settlement results summarized in Markdown, with cited rules and a draft itemized statement.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deadlines, deduction assessments, interest and refund calculations, penalty exposure, citations, and a repeatable result hash when requested.]

## Skill Version(s):

1.0.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
