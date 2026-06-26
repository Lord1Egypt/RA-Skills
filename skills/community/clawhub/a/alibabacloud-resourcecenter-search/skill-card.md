## Description: <br>
Alibaba Cloud Resource Center skill for cross-region, cross-product, and cross-account resource inventory, search, statistics, and service enablement or disablement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operators use this skill to inspect Alibaba Cloud Resource Center inventory, find resource type codes, search or count resources, view resource configurations and tags, and manage Resource Center activation with explicit user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to use a local Alibaba Cloud CLI profile for Resource Center operations. <br>
Mitigation: Use read-only RAM policies where possible, avoid long-lived access keys in commands or logs, and confirm credentials are configured outside the agent session. <br>
Risk: Setup steps may modify local CLI tooling or plugin behavior. <br>
Mitigation: Install or update Aliyun CLI yourself when possible, review plugin changes before enabling automatic plugin installation, and keep plugins current deliberately. <br>
Risk: Cross-account searches and Resource Center disable operations can expose broad inventory scope or disrupt resource visibility. <br>
Mitigation: Require explicit confirmation for cross-account scopes and any disable operation, and use the most specific Resource Directory scope that satisfies the request. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-resourcecenter-search) <br>
- [Related Resource Center APIs](references/related-apis.md) <br>
- [RAM Permission Policies](references/ram-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Resource Center Error Codes](references/error-codes.md) <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-producing helper script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a configured Alibaba Cloud CLI profile and should favor read-only RAM policies for search and statistics workflows.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
