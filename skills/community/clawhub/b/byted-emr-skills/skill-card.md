## Description: <br>
Byted EMR Skills helps agents administer Volcengine E-MapReduce environments across EMR on ECS, EMR on VKE, and EMR Serverless, including clusters, queues, jobs, logs, monitoring, and EMR Agent diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robinliew](https://clawhub.ai/user/robinliew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform operators use this skill to manage Volcengine EMR resources, submit and monitor big-data jobs, retrieve logs and reports, and invoke EMR Agent diagnostics from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global; runtime availability depends on configured Volcengine EMR regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer real Volcengine EMR resources, including broad operational changes. <br>
Mitigation: Use it only for intended EMR administration tasks and require human confirmation before restarts, deletes, privilege grants, password changes, configuration updates, resource changes, job submissions, or report and history retrieval. <br>
Risk: The skill handles Volcengine credentials and may pass job or configuration data through commands and scripts. <br>
Mitigation: Use least-privilege, preferably temporary credentials, and avoid placing secrets in command lines, job definitions, or configuration payloads. <br>
Risk: The Serverless SDK installer can download and install a wheel from a remote source. <br>
Mitigation: Verify the SDK wheel source and integrity before installation, or provide a vetted local wheel. <br>


## Reference(s): <br>
- [Byted EMR Skills on ClawHub](https://clawhub.ai/robinliew/byted-emr-skills) <br>
- [EMR Serverless Queue Guide](artifact/references/emr_serverless/queue/emr_serverless_queue_guide.md) <br>
- [EMR Serverless Job Guide](artifact/references/emr_serverless/job/emr_serverless_job_guide.md) <br>
- [EMR Serverless Job Instance Guide](artifact/references/emr_serverless/job_instance/emr_serverless_job_instance_guide.md) <br>
- [EMR Serverless Compute Guide](artifact/references/emr_serverless/compute/emr_serverless_compute_guide.md) <br>
- [EMR Serverless Privilege Guide](artifact/references/emr_serverless/privilege/emr_serverless_privilege_guide.md) <br>
- [EMR Agent Guide](artifact/references/emr_agent/emr_agent_guide.md) <br>
- [EMR on ECS Cluster Guide](artifact/references/emr_on_ecs/cluster/emr_on_ecs_cluster_guide.md) <br>
- [EMR on ECS Application Guide](artifact/references/emr_on_ecs/application/emr_on_ecs_application_guide.md) <br>
- [EMR on ECS Application Configuration Guide](artifact/references/emr_on_ecs/application_config/emr_on_ecs_application_config_guide.md) <br>
- [EMR on ECS User Guide](artifact/references/emr_on_ecs/user/emr_on_ecs_user_guide.md) <br>
- [EMR on ECS User Group Guide](artifact/references/emr_on_ecs/user_group/emr_on_ecs_user_group_guide.md) <br>
- [EMR on VKE Guide](artifact/references/emr_on_vke/emr_on_vke_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute Volcengine EMR API operations when the agent runs the provided scripts.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
