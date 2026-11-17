## Description:

Use for pre-sign safety: allowance audits, route and health sentinel checks, and policy scans of unsigned transactions; it returns verdicts and never signs or broadcasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parmasanandgarlic](https://clawhub.ai/user/parmasanandgarlic)

### License/Terms of Use:

MIT-0

## Use Case:

DeFi users and agent operators use Camp Guard to review token approvals, swap routes, account health, and unsigned transactions before signing. Its pass, review, or halt verdicts guide whether a workflow can proceed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that wallet, allowance, route, and unsigned-transaction details may be sent to FarmDash without clear user disclosure.

Mitigation: Before use, review what information will be sent and proceed only if you are comfortable sharing it with FarmDash.

Risk: The security scan was partial, and some local references could not be resolved, so its findings may be incomplete.

Mitigation: Treat the scan as incomplete and review unresolved references and the skill's behavior before relying on its verdicts.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/parmasanandgarlic/skills/farmdash-camp-guard)
- [Canonical FarmDash Camp Guard manual](https://www.farmdash.one/openclaw-skills/farmdash-camp-guard/SKILL.md)
- [FarmDash agent integration documentation](https://www.farmdash.one/docs)
- [FarmDash OpenAPI contract](https://www.farmdash.one/agents/openapi.yaml)
- [FarmDash security and authority boundaries](https://www.farmdash.one/security)
- [FarmDash fees and commercial terms](https://www.farmdash.one/fees)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, JSON]

**Output Format:** [Structured JSON verdicts and risk flags with concise safety guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts are limited to supplied-data policy checks; transaction simulation is not run.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
