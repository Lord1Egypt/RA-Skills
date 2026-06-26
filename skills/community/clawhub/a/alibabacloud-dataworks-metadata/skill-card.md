## Description: <br>
DataWorks metadata Skill for Alibaba Cloud that helps agents browse Data Map metadata and perform guarded, non-destructive metadata updates through Aliyun CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, data engineers, and cloud operators use this skill to inspect Alibaba Cloud DataWorks catalogs, databases, tables, columns, partitions, lineage, datasets, versions, and metadata collections. They can also ask the agent to propose guarded, non-destructive metadata updates with explicit confirmation before writes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide non-destructive writes to DataWorks metadata, including business metadata, lineage, datasets, versions, collections, and collection entities. <br>
Mitigation: Use a least-privilege Aliyun profile, start with read-only RAM permissions unless writes are needed, and require explicit user confirmation before every write. <br>
Risk: Credentials or access keys could be exposed if an agent prints or passes literal secrets in CLI commands. <br>
Mitigation: Check credential status with the allowed Aliyun CLI profile command only; never read, echo, print, or place literal AK/SK values in commands. <br>
Risk: A write command could time out after partially succeeding, creating duplicate resources if retried blindly. <br>
Mitigation: After write timeouts or ambiguous errors, re-check state with the matching list or get command before retrying or accepting the existing resource. <br>
Risk: The skill temporarily enables Aliyun CLI AI-Mode and sets a skill-specific user agent. <br>
Mitigation: Disable AI-Mode when the DataWorks task is complete so the skill user agent does not carry over into unrelated CLI usage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-dataworks-metadata) <br>
- [Aliyun CLI installation documentation](https://help.aliyun.com/document_detail/121541.html) <br>
- [Entity ID Format Reference](references/entity-id-formats.md) <br>
- [RAM Policies - DataWorks Metadata](references/ram-policies.md) <br>
- [Related CLI Commands - DataWorks Metadata](references/related-commands.md) <br>
- [Verification Method - DataWorks Metadata](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require user-confirmed parameters, Aliyun CLI timeouts, and explicit confirmation before non-destructive writes.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
