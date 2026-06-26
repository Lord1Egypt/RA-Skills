## Description: <br>
Query Catalog, database, and table metadata resources in Alibaba Cloud Data Lake Formation (DLF) through read-only DLF OpenAPI Python SDK operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data platform engineers use this skill to inspect Alibaba Cloud DLF Catalog, database, and table metadata, including table schemas, while staying within read-only list and get operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on Alibaba Cloud credentials and DLF permissions, so overly broad account access could expose more metadata than intended. <br>
Mitigation: Use the documented read-only RAM and DLF data permissions, rely on the default credential chain, and do not ask users to reveal access keys. <br>
Risk: Detailed table and database queries can be heavier than lightweight list actions and may retrieve more metadata than the user requested. <br>
Mitigation: Default to list actions for names, IDs, and search, and use detail or schema actions only when explicitly requested. <br>
Risk: VirusTotal was pending in the available ClawHub scan evidence. <br>
Mitigation: Review setup prompts before granting credentials or filesystem access, and install only when the skill description matches the intended use. <br>


## Reference(s): <br>
- [DLF API overview](https://help.aliyun.com/zh/dlf/dlf-2-0/developer-reference/api-dlfnext-2025-03-10-overview) <br>
- [DLF product documentation](https://help.aliyun.com/zh/dlf/dlf-2-0) <br>
- [Alibaba Cloud credential configuration](https://help.aliyun.com/document_detail/378659.html) <br>
- [Python SDK PyPI](https://pypi.org/project/alibabacloud-dlfnext20250310/) <br>
- [DLF Read-only Query API Reference](references/related-apis.md) <br>
- [RAM Permissions Required](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with Python command examples and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only metadata queries return JSON objects or paginated JSON lists; errors return JSON with an error message and optional hint.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
