## Description:

A Chinese-language architecture governance skill that evaluates system health across six dimensions, identifies technical debt and risk, and produces governance tasks and reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys)

### License/Terms of Use:


## Use Case:

Developers, architects, and governance teams use this skill to assess architecture health, compare systems, prioritize technical debt, and prepare governance reports or work plans.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext HTTP credential examples may be copied into real integrations.

Mitigation: Replace HTTP examples with HTTPS endpoints and environment-managed tokens before using integration examples.

Risk: The bundled health-check script uses simulated metrics and is not ready as an authoritative CI or governance signal.

Mitigation: Fix and integrate the script with real metric sources before relying on it for CI gates or governance reporting.

Risk: The report output option can overwrite the file at the specified path.

Mitigation: Choose output paths deliberately and avoid pointing the script at important existing files.

## Reference(s):

- [Architecture Governance Evaluation Framework](references/evaluation-framework.md)
- [Metrics Definition and Collection Plan](references/metrics.md)
- [Architecture Governance Playbook](references/governance-playbook.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, task lists, assessment checklists, and concise command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled script can optionally write a Markdown report to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
