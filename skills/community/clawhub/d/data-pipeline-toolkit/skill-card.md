## Description: <br>
Create, schedule, and monitor ETL pipelines that extract from APIs, databases, files, and streams, then transform and load data to warehouses, databases, and APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and data engineers use this skill to outline CLI-driven ETL workflows for extracting, transforming, loading, scheduling, and monitoring data pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Quick-start commands invoke ./pipeline.sh, but no pipeline.sh file is included in the artifact. <br>
Mitigation: Confirm the exact script path and source before running any quick-start command, and test in an isolated workspace first. <br>
Risk: ETL workflows may touch databases, APIs, cloud storage, scheduled jobs, and credentials. <br>
Mitigation: Use non-production test data, narrowly scoped credentials, and verify how any schedules can be found and removed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only ETL workflow guidance; no executable pipeline script is included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
