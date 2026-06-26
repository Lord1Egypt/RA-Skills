## Description: <br>
Query DTS task status and details across Alibaba Cloud regions, with filters for region, instance ID, and job name. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inventory Alibaba Cloud DTS migration, synchronization, and subscription tasks, check their status, and filter results by region, instance ID, or job name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill without filters can expose broad Alibaba Cloud DTS task metadata across supported regions. <br>
Mitigation: Use a least-privilege RAM policy limited to dts:DescribeDtsJobs and apply --region, --instance-id, or --job-name when a full account-wide inventory is unnecessary. <br>
Risk: The skill uses local Aliyun CLI credentials to query DTS metadata. <br>
Mitigation: Run it only in environments where those credentials are approved for read-only DTS inventory access. <br>


## Reference(s): <br>
- [RAM Permissions for DTS Task Query](references/ram-policies.md) <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-dts-task-query) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with Chinese summaries and task detail tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports all matching DTS tasks without truncation; may include cloud task metadata from every supported region unless filters are used.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
