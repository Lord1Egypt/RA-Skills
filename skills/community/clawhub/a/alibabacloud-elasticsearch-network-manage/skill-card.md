## Description: <br>
Alibaba Cloud Elasticsearch Instance Network Management Skill for managing ES instance network configurations, including triggering network changes, Kibana PVL network, white IP lists, HTTPS settings, and Kibana SSO authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud administrators, DevOps engineers, and developers use this skill to plan and execute Alibaba Cloud Elasticsearch network, allowlist, HTTPS, and Kibana SSO configuration changes through Aliyun CLI workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer Alibaba Cloud Elasticsearch network, allowlist, HTTPS, SSO, and persistent Aliyun CLI settings. <br>
Mitigation: Use a dedicated least-privilege RAM user or role scoped to the exact instance, prefer temporary credentials, and review every command body before execution. <br>
Risk: Opening public access, replacing allowlists, disabling HTTPS, or disabling SSO can weaken access controls. <br>
Mitigation: Require explicit human approval before those operations and verify the resulting instance configuration after changes. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/sdk-team/alibabacloud-elasticsearch-network-manage) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Aliyun CLI setup](https://aliyuncli.alicdn.com/setup.sh) <br>
- [Alibaba Cloud RAM AccessKey management](https://ram.console.aliyun.com/manage/ak) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit human confirmation for user-customizable parameters and sensitive network or authentication changes.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
