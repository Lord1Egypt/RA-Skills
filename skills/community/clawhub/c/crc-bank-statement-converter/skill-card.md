## Description:

Converts bank statement Excel and CSV exports into a 9-column regulatory reporting workbook package.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qiqikuaidianpao](https://clawhub.ai/user/qiqikuaidianpao)

### License/Terms of Use:

MIT-0

## Use Case:

Finance, compliance, and operations users use this skill to batch-normalize bank statement exports from multiple banks and accounts into a standard reporting package. It is intended for Excel and CSV bank statement conversion, not for repairing encrypted or damaged files or analyzing transaction trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes sensitive financial spreadsheets, and server security evidence flags material safety issues for this use case.

Mitigation: Run it in an isolated environment with a narrow workspace, avoid privileged execution, and process only files the user is authorized to handle.

Risk: Generated spreadsheets may be unsafe to open or share until formula sanitization is added.

Mitigation: Treat generated workbooks as untrusted output and review or sanitize them before opening in privileged spreadsheet environments or distributing them.

Risk: Temporary-file handling is called out by server security guidance as needing safer implementation.

Mitigation: Avoid shared-machine execution for sensitive statements and run one conversion job at a time in a private workspace until safer temporary-file handling is added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qiqikuaidianpao/skills/crc-bank-statement-converter)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance with bash commands; generated ZIP containing Excel workbooks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a summary workbook and one 9-column .xlsx workbook per source statement.]

## Skill Version(s):

1.5.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
