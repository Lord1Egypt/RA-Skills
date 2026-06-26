## Description: <br>
Evaluates system architecture health across six governance dimensions and produces scores, risk priorities, governance tasks, and reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerry-guo-mys](https://clawhub.ai/user/jerry-guo-mys) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, architects, and engineering governance teams use this skill to assess architecture health, compare systems, identify technical debt and risks, and plan governance work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional Python helper can write a report to a path chosen by the user. <br>
Mitigation: Choose the output path deliberately and avoid overwriting important files. <br>
Risk: Metric collection examples reference internal service, CI, tracing, and incident systems. <br>
Mitigation: Adapt those examples only for systems where you have authorization and least-privilege credentials. <br>
Risk: Architecture scores and governance priorities depend on the quality of supplied metrics and manual assessments. <br>
Mitigation: Review the generated findings with system owners before using them for planning or governance decisions. <br>


## Reference(s): <br>
- [Architecture Governance Evaluation Framework](references/evaluation-framework.md) <br>
- [Architecture Governance Playbook](references/governance-playbook.md) <br>
- [Metrics Definition and Collection Plan](references/metrics.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports, task lists, checklists, and optional shell command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The optional helper can write a Markdown report to a user-selected output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
