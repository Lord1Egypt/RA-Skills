## Description:

Use for pre-sign safety: allowance audits, route/health sentinel checks, policy scan of unsigned transactions. Verdicts only; never signs or broadcasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill to review ERC-20 allowances, DeFi route or position risk, and unsigned transactions before proceeding toward signing. It returns pass, review, or halt guidance and does not sign or broadcast transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Risk checks transmit submitted wallet, allowance, route, or unsigned transaction data to FarmDash; quoted route checks can also send route parameters to external quote and pricing providers.

Mitigation: Send only the data needed for the requested check, omit the optional wallet address when possible, and review the FarmDash privacy policy before sharing unpublished transaction details.

Risk: A pass covers supplied-data policy checks and is not a smart-contract audit or RPC execution simulation.

Mitigation: Review returned flags and run an independent wallet, RPC, or Tenderly-style simulation before broadcast.

Risk: The security scan reported no findings but had medium confidence because analysis was partial and some local path-like references could not be resolved.

Mitigation: Review the skill and its unresolved references before installation or use.

## Reference(s):

- [FarmDash Camp Guard skill manual](https://www.farmdash.one/agents/skills/farmdash-camp-guard)
- [FarmDash agent documentation](https://www.farmdash.one/docs)
- [FarmDash Privacy Policy](https://www.farmdash.one/privacy)
- [FarmDash Security and Authority Boundaries](https://www.farmdash.one/security)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance, JSON]

**Output Format:** [Structured risk verdicts with flags and safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only; verdicts are pass, review, or halt and do not sign or broadcast transactions.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
