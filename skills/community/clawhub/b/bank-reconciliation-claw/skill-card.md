## Description:

银行流水对账虾 helps agents reconcile local bank statement and order files, identify unmatched rows, amount differences, duplicate entries, and date offsets, and generate reconciliation reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Finance operators, accountants, and developers use this skill to compare bank statement exports with system order data and produce a local Excel reconciliation report for review. It is intended for explicit local files supplied by the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Preview mode can print raw rows from sensitive financial files.

Mitigation: Use preview only on sanitized samples or in private logs; avoid preview on real data unless output is protected.

Risk: Security evidence says invoice, Feishu export, historical, and multi-account capabilities are overstated.

Mitigation: Treat those workflows as unsupported or requiring manual review and companion tooling; validate any report before accounting use.

Risk: The skill processes financial records and depends on local Python packages.

Mitigation: Run it only in an isolated local environment with pinned pandas and openpyxl dependencies and explicit user-provided files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tujinsama/skills/bank-reconciliation-claw)
- [Reconciliation rules](references/reconciliation-rules.md)
- [Field mapping](references/field-mapping.md)
- [Desensitization rules](references/desensitization-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands and generated Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can write an Excel report with summary, matched-detail, and anomaly sheets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
