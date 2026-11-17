## Description:

Records AI-assisted tasks and file changes, produces verification reports, and documents approval gates for high-risk actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to record who initiated an AI-assisted task, track file changes, and check the resulting audit records. It also helps document human approval requirements for actions such as sending, deleting, or publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approval safeguards and audit checks may provide less protection than expected; successful verification does not prove that every action was recorded or approved.

Mitigation: Keep independent approval controls for sending, deletion, payments, and publishing, and review the host agent's enforcement process.

Risk: Logs may expose sensitive information, and report generation may overwrite files.

Mitigation: Use a narrow project directory, validate report destinations, and review and redact logs before sharing or committing them.

Risk: Testing against real files or recipients may cause unintended changes or external actions.

Mitigation: Test with disposable files and mocked recipients.

## Reference(s):

- [Evidence chain template](artifact/references/01-证据链模板.md)
- [Approval gate checklist](artifact/references/02-门禁清单.md)
- [Examples and boundaries](artifact/references/03-反例与边界.md)
- [Project governance template](artifact/references/04-项目治理骨架.md)
- [LGD theory](https://github.com/zhaoxinghua09-cell/LGD)
- [Formal paper](https://doi.org/10.5281/zenodo.22456647)
- [Protocol and reference implementation](https://github.com/zhaoxinghua09-cell/uibc-core)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Files, Guidance]

**Output Format:** [Python command-line usage, JSONL audit records, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates local task registries, evidence logs, gate records, and verification reports in the selected project directory.]

## Skill Version(s):

1.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
