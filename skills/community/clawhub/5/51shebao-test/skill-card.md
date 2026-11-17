## Description:

HR 税费计算器用于本地估算工资个税、税后收入、劳务报酬、稿酬、特许权使用费和离职补偿金个税，并支持部分税后反推税前场景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzzzzmh](https://clawhub.ai/user/zzzzzmh)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, HR teams, and agents supporting China-oriented payroll questions use this skill to calculate or estimate individual income tax, take-home pay, remuneration tax, royalty tax, author remuneration tax, and severance compensation tax from user-provided inputs.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Tax rules, thresholds, and local social insurance or average salary inputs may change, making calculator results stale or incomplete.

Mitigation: Treat outputs as estimates and verify current official tax rules, local social insurance figures, and local average salary values before relying on results.

Risk: Salary, compensation, deduction, and pension figures may be sensitive personal or employment data.

Mitigation: Run the disclosed local scripts without network access and avoid sharing more salary details than needed for the calculation.

Risk: Missing user-provided social insurance, housing fund, deduction, or city average salary values can materially change the estimate.

Mitigation: Ask users to provide wage-slip, local social insurance app, statistics bureau, or human-resources bureau values, and clearly label default-zero calculations as estimates.

## Reference(s):

- [计算规则参考](references/tax-rules.md)
- [ClawHub skill page](https://clawhub.ai/zzzzzmh/skills/51shebao-test)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON calculator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Python standard library scripts; estimates depend on current tax rules and user-provided payroll, deduction, and local average salary inputs.]

## Skill Version(s):

0.2.0 (source: ClawHub release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
