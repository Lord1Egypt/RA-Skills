## Description: <br>
Thoroughly audit Tasks.md + Flatnotes for drift and accuracy; use GitHub (gh CLI) as source of truth to detect stale notes/cards and missing links. Produces a report and an optional fix plan. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[branexp](https://clawhub.ai/user/branexp) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to audit a local Tasks.md and Flatnotes workflow against GitHub pull request state, identify stale or missing project records, and produce a report with an optional fix plan. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auditor reads local Tasks.md and Flatnotes directories, which may contain private project names, paths, task titles, and planning details. <br>
Mitigation: Set TASKS_ROOT and FLATNOTES_ROOT only to directories intended for audit, and review generated tmp reports before sharing them. <br>
Risk: GitHub checks use the locally authenticated gh account, so results depend on that account's repository access and identity. <br>
Mitigation: Confirm the active gh authentication context before running the audit. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/branexp/flatnotes-tasksmd-github-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown and JSON audit reports with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report files are written under tmp/ when the bundled auditor is run with --write.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
