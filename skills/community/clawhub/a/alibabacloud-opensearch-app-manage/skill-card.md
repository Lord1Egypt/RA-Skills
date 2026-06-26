## Description: <br>
Alibaba Cloud OpenSearch instance management skill for creating, listing, and describing OpenSearch instances. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to manage Alibaba Cloud OpenSearch instances through Aliyun CLI workflows, including instance creation, listing, and detail lookup. It is intended for accounts with appropriate OpenSearch RAM permissions and configured Alibaba Cloud credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Create operations can provision persistent billable Alibaba Cloud OpenSearch resources. <br>
Mitigation: Prefer dryRun first, require explicit approval before create commands, use idempotency tokens, and clean up test instances promptly in the OpenSearch console. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials or an authorized profile to manage OpenSearch. <br>
Mitigation: Use a dedicated least-privilege RAM user or temporary role, verify the active Aliyun profile before commands run, and avoid exposing AccessKey values in conversation or logs. <br>
Risk: Installation and plugin update steps can change local CLI tooling. <br>
Mitigation: Use an official package manager or a downloaded installer that can be verified, and review CLI/plugin updates before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/alibabacloud-opensearch-app-manage) <br>
- [CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification method](references/verification-method.md) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [Aliyun CLI documentation](https://help.aliyun.com/zh/cli/) <br>
- [RAM policy overview](https://help.aliyun.com/document_detail/93732.html) <br>
- [OpenSearch authorization rules](https://help.aliyun.com/zh/open-search/industry-algorithm-edition/authorization-rules-of-applications) <br>
- [OpenSearch console](https://opensearch.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Aliyun CLI command examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require Aliyun CLI 3.3.3 or later, configured Alibaba Cloud credentials, OpenSearch RAM permissions, and explicit user confirmation for customizable parameters.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
