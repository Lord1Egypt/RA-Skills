## Description: <br>
Alibaba Cloud EMR Serverless StarRocks assistant for cluster connection, schema design, data ingestion, SQL development and tuning, and cluster health diagnostics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill for day-to-day StarRocks work on Alibaba Cloud EMR Serverless, including connection setup, table design, ingestion planning, SQL tuning, materialized views, and operational diagnostics. It is not intended for StarRocks instance lifecycle control or non-StarRocks Alibaba Cloud products. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist StarRocks database credentials locally and attempt environment-based login. <br>
Mitigation: Use a least-privilege StarRocks account, avoid preloading SR_PASSWORD unless non-interactive login is intended, and remove ~/.starrocks profiles when access is no longer needed. <br>
Risk: The skill can install tooling and operate against a live StarRocks environment. <br>
Mitigation: Review the skill before deployment, inspect proposed commands, and require explicit confirmation before non-READ SQL or production-impacting operations. <br>
Risk: Inline credential or remote-code examples may be unsafe if copied directly into production. <br>
Mitigation: Replace example credentials with secure secret handling and use trusted artifact sources before production use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-emr-starrocks-assistant) <br>
- [Connection Guide](artifact/references/connect.md) <br>
- [Schema Design Guide](artifact/references/schema.md) <br>
- [Data Import Guide](artifact/references/data-import.md) <br>
- [SQL Development and Tuning Guide](artifact/references/sql.md) <br>
- [Diagnostics Guide](artifact/references/diagnostics.md) <br>
- [RAM Policies Reference](artifact/references/ram-policies.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or run StarRocks CLI commands using the user's configured credentials and privileges.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
