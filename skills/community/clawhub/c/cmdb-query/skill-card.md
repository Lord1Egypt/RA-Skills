## Description: <br>
Queries internal CMDB asset data by resource type, including hosts, applications, databases, and name-filtered records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jbhasbc](https://clawhub.ai/user/jbhasbc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Authorized internal operators, developers, and infrastructure teams use this skill to query CMDB assets and inspect resource records across host, application, database, network, storage, account, and billing models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release exposes shared internal credentials for an internal CMDB. <br>
Mitigation: Install only with authorization, rotate or replace the exposed account, and require user- or vault-supplied scoped credentials before use. <br>
Risk: The skill can query highly sensitive records, including private keys, bastion access data, account forms, and billing records. <br>
Mitigation: Restrict accessible models by role and redact or block sensitive record classes before general use. <br>
Risk: The helper code disables TLS certificate verification when calling the CMDB API. <br>
Mitigation: Enable proper TLS verification and configure trusted internal CA certificates before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jbhasbc/cmdb-query) <br>
- [CMDB homepage](https://10.255.227.233/cmdb) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown guidance with curl and jq examples plus Python helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for documented command examples; Python helper uses HTTP requests to the CMDB API.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
