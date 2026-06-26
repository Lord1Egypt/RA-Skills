## Description: <br>
ADBPG Knowledge Base Management helps agents create knowledge bases, upload documents, search content, and run Q&A workflows for Alibaba Cloud AnalyticDB PostgreSQL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud AnalyticDB PostgreSQL knowledge bases through Aliyun CLI and SDK workflows. It supports creating namespaces and document collections, uploading documents, searching indexed content, and answering questions from knowledge-base data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill works with Alibaba Cloud database resources and sensitive credentials, including manager and namespace passwords. <br>
Mitigation: Use least-privilege RAM credentials, prefer temporary credentials or a secure secret path, and avoid pasting long-lived passwords into chat or command lines. <br>
Risk: Knowledge-base creation can trigger paid Alibaba Cloud resource usage. <br>
Mitigation: Require explicit user approval for region, instance, size, cost expectations, and cleanup plan before creating or modifying resources. <br>
Risk: Incorrect parameters or missing permissions can operate on the wrong instance or fail after partial workflow progress. <br>
Mitigation: Confirm user-customizable parameters before modification commands and verify RAM permissions before running write operations. <br>


## Reference(s): <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Interaction Guidelines](references/interaction-guidelines.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Chinese Skill Reference](references/SKILL.zh-CN.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown with Aliyun CLI commands, Python SDK command examples, configuration guidance, and status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud operation plans, parameter confirmations, upload job identifiers, search results, and Q&A responses.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
