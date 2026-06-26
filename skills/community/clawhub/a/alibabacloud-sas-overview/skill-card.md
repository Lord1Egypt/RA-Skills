## Description: <br>
Queries Alibaba Cloud Security Center (SAS) overview data, including security score, asset status, risk governance, asset risk trends, and billing information. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security operators and developers use this skill to retrieve read-only Alibaba Cloud SAS overview metrics, WAF block statistics, asset risk trends, and SAS billing or subscription status through Aliyun CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup may make persistent changes to the local Aliyun CLI and plugin state. <br>
Mitigation: Review the setup steps first, prefer package-manager or manually verified CLI installation, and run plugin updates only in an environment where CLI state changes are acceptable. <br>
Risk: Remote script execution through curl | bash can run unreviewed installer code. <br>
Mitigation: Avoid piping remote scripts directly to a shell; download from the official source, inspect or verify the installer, and execute it explicitly. <br>
Risk: Alibaba Cloud credentials and returned security or billing data are sensitive. <br>
Mitigation: Use least-privilege read-only RAM permissions, verify credentials only through safe CLI status checks, and avoid sharing access keys or command outputs containing sensitive account data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-sas-overview) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related APIs](references/related-apis.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Alibaba Cloud queries; results may include security posture, asset, and billing data from configured Aliyun profiles.] <br>

## Skill Version(s): <br>
0.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
