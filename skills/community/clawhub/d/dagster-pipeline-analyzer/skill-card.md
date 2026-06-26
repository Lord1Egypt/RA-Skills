## Description: <br>
Analyze Dagster pipelines and software-defined assets for quality, scheduling, partitioning, IO managers, resource configuration, and observability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charlie-morrison](https://clawhub.ai/user/charlie-morrison) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data platform engineers use this skill to review Dagster projects, audit asset graphs, analyze partitioning and scheduling patterns, and identify reliability, security, and observability gaps before deployment or during maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides repository maintenance and audit tasks that may involve local commands or changes to project configuration. <br>
Mitigation: Review proposed commands and remediation changes before execution or merge, and run normal code review and scanning before deployment. <br>
Risk: Analysis findings may be incomplete or inaccurate if the provided Dagster project context is partial. <br>
Mitigation: Provide the Dagster project root, dagster.yaml, workspace.yaml, and relevant version information, then validate recommendations against the actual deployment environment. <br>


## Reference(s): <br>
- [Dagster Pipeline Analyzer on ClawHub](https://clawhub.ai/charlie-morrison/dagster-pipeline-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown analysis report with command examples, health scoring, issue lists, and remediation code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include asset graph summaries, category scores, critical findings, warnings, and recommended Dagster configuration changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
