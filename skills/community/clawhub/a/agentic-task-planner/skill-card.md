## Description: <br>
临床科研任务总调度器，将研究任务拆解为多步执行计划，并依次调度证据检索、数据映射、统计分析和导出治理等步骤。 <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[emergenceronearth](https://clawhub.ai/user/emergenceronearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinical research platform users and developers use this skill to run a complete mock research-analysis workflow, from task planning through evidence grounding, cohort mapping, statistical summary, and export-governance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow is designed around local mock_data files and a localhost monitoring endpoint, so it may fail or produce misleading results if those demo resources are missing or replaced with unsupported data. <br>
Mitigation: Use it only in an environment with the expected mock_data files and monitoring service, and verify any substituted data before acting on results. <br>
Risk: Clinical research workflows can expose institutional or patient-related details if real data is used without controls. <br>
Mitigation: Confirm authorization before using real institutional or patient-related data, and ensure the local reporting endpoint does not store sensitive task details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/emergenceronearth/agentic-task-planner) <br>
- [Publisher profile](https://clawhub.ai/user/emergenceronearth) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured Markdown with inline shell commands and progress summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local mock data files and reports workflow progress to a localhost monitoring endpoint.] <br>

## Skill Version(s): <br>
0.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
