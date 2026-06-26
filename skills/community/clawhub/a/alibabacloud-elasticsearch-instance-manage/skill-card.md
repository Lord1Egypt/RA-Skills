## Description: <br>
Alibaba Cloud Elasticsearch Instance and Config Management Skill for managing Elasticsearch instance lifecycle operations and instance-side configuration such as snapshots and analyzer dictionaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to generate Aliyun CLI guidance and commands for Alibaba Cloud Elasticsearch instance creation, lookup, restart, upgrade or downgrade, node inspection, snapshot configuration, and analyzer dictionary management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose disruptive cloud operations such as restart, force restart, upgrade, downgrade, snapshot changes, and dictionary replacement. <br>
Mitigation: Use explicit maintenance-window confirmation and verify region, instance ID, operation type, and intended configuration before executing write commands. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials or OAuth-backed access. <br>
Mitigation: Use a least-privilege RAM user or temporary role, rely on environment variables or preconfigured CLI profiles, and do not paste production secrets into chat. <br>
Risk: Dictionary update APIs use full-list overwrite behavior that can delete existing dictionary files if the target list is incomplete. <br>
Mitigation: List current dictionaries first, build the complete desired final list, and preserve existing files with the documented origin source type where needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-elasticsearch-instance-manage) <br>
- [Instance lifecycle APIs](references/instance-manage.md) <br>
- [Instance configuration APIs](references/config-manage.md) <br>
- [RAM permission policies](references/ram-policies.md) <br>
- [Verification methods](references/verification-method.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [Node specifications by region](references/node-specifications-by-region.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Alibaba Cloud Elasticsearch product page](https://www.aliyun.com/product/bigdata/elasticsearch) <br>
- [Alibaba Cloud Elasticsearch API reference](https://next.api.aliyun.com/product/elasticsearch) <br>
- [Aliyun CLI documentation](https://help.aliyun.com/zh/cli/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown with Aliyun CLI command blocks and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require user-provided region, instance identifiers, configured Aliyun credentials, and a per-session user-agent value.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
