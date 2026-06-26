## Description: <br>
Create an agent platform instance in DMS via Alibaba Cloud OpenAPI. Supports Simple Mode and Advanced Mode. Use this skill when the user wants to provision, deploy, or set up a new Dify instance on Alibaba Cloud DMS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to configure credentials, collect network and resource parameters, run a DMS availability pre-check, and generate the Alibaba Cloud CLI and Python API calls needed to provision a Dify instance on Alibaba Cloud DMS. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Provisioning can create Alibaba Cloud resources and costs when DryRun is disabled. <br>
Mitigation: Run with DryRun=true first, review the request and expected costs, and switch to DryRun=false only after explicit confirmation. <br>
Risk: The workflow requires cloud credentials and service passwords. <br>
Mitigation: Use a dedicated least-privilege RAM role, avoid exposing secrets in shell history or shared terminal logs, and follow the credential handling guidance in the release evidence. <br>


## Reference(s): <br>
- [RAM Permission Configuration](references/ram-policies.md) <br>
- [Alibaba Cloud Python SDK v2: Manage Access Credentials](https://help.aliyun.com/zh/sdk/developer-reference/v2-manage-python-access-credentials#3ca299f04bw3c) <br>
- [DMS Permission Management](https://help.aliyun.com/zh/dms/user-guide/permission-management) <br>
- [DMS CreateDifyInstance API](https://api.aliyun.com/api/dms-enterprise/2018-11-01/CreateDifyInstance) <br>
- [DMS ListInstances API](https://api.aliyun.com/api/dms-enterprise/2018-11-01/ListInstances) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a DMS availability pre-check, Simple Mode and Advanced Mode provisioning flows, and a recommended DryRun=true validation pass before provisioning.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
