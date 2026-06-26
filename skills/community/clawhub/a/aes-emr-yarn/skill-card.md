## Description: <br>
Analyzes YARN resource consumption for Alibaba Cloud EMR clusters using SSH and EMR API data, then produces a Markdown report with utilization trends, queue usage, idle or overprovisioning risks, fragmentation indicators, and capacity recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qinyafei123](https://clawhub.ai/user/qinyafei123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data platform engineers, and operations teams use this skill to inspect YARN cluster load, resource utilization, node and application status, and capacity risks for EMR environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The packaged artifact includes real-looking cloud AccessKey values and a root SSH password. <br>
Mitigation: Do not run the skill as packaged; rotate exposed credentials, remove secrets from the artifact, and provide credentials through a protected runtime configuration or secret store. <br>
Risk: The skill performs remote SSH and EMR API collection against configured infrastructure. <br>
Mitigation: Use a read-only least-privilege account, verify the SSH host key, restrict network scope, and review the remote commands before execution. <br>
Risk: Config, cookie, and log files may contain sensitive operational data. <br>
Mitigation: Apply restrictive file permissions, avoid logging secrets, and limit retention and access for generated local files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qinyafei123/aes-emr-yarn) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/qinyafei123) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown report with tables, utilization metrics, status summaries, and operational recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cluster ID, analysis window, CPU and memory utilization, node status, application counts, system resource details, and optimization guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
