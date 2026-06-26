## Description: <br>
Audits up to five contracts through the dyinsight.cn streaming API using either public file URLs or multipart uploads, with a required Party A or Party B review perspective and API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tzz-v](https://clawhub.ai/user/tzz-v) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit contract files or contract URLs for streaming contract audit results from a remote service. It is intended for batch review workflows where the user chooses the Party A or Party B perspective before analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected contracts to dyinsight.cn for remote audit, so contract contents may include confidential, privileged, or regulated information. <br>
Mitigation: Install and use only when the user trusts dyinsight.cn and is authorized to share the contracts; redact unnecessary sensitive data where possible. <br>
Risk: The local config file contains an API key required by the remote service. <br>
Mitigation: Keep config.json private, avoid committing real API keys, and confirm the key is configured before making live requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tzz-v/contract-audit-stream) <br>
- [Publisher profile](https://clawhub.ai/user/tzz-v) <br>
- [Service endpoint](https://dyinsight.cn/api/v1/skills/contract/audit) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown, JSON] <br>
**Output Format:** [Markdown guidance with curl examples and streaming JSON event content from the remote API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces SSE progress, error, and completion events; final audit results are returned in streamed JSON content.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
