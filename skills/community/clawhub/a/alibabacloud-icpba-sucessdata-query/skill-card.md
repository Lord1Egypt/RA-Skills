## Description: <br>
Alibaba Cloud ICP Filing Success Data Query Skill. Use for querying ICP filing success information including entity, website, app details and risk alerts after successful filing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and Alibaba Cloud account operators use this skill to query ICP filing success data, including entity, website, app, and filing-risk information after successful filing. <br>

### Deployment Geography for Use: <br>
China (Alibaba Cloud ICP filing context) <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Alibaba Cloud credentials and can access sensitive ICP filing data. <br>
Mitigation: Run it only with a dedicated least-privilege RAM role or user limited to beian:QuerySuccessIcpData, and never paste or log access keys. <br>
Risk: The skill output may include entity details, responsible-person names, domains, app records, and filing-risk information. <br>
Mitigation: Avoid logging full results, redact sensitive fields before sharing output, and limit access to users who need ICP filing data. <br>
Risk: The artifact includes provider tooling update steps and RAM policy setup examples beyond the read-only query path. <br>
Mitigation: Review commands before execution and run policy creation or attachment steps only during deliberate administrator setup. <br>


## Reference(s): <br>
- [RAM Policies for ICP Filing Success Query](references/ram-policies.md) <br>
- [Related Commands for ICP Filing Success Query](references/related-commands.md) <br>
- [Verification Method for ICP Filing Success Query](references/verification-method.md) <br>
- [Aliyun CLI Installation & Configuration Guide](references/cli-installation-guide.md) <br>
- [Python Common SDK Usage for ICP Filing Query](references/common-sdk-usage.md) <br>
- [Error Handling for ICP Filing Success Query](references/error-handling.md) <br>
- [Alibaba Cloud RAM Console](https://ram.console.aliyun.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash and Python code blocks, plus JSON API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May print ICP filing records, entity details, website and app data, and risk remediation suggestions returned by Alibaba Cloud.] <br>

## Skill Version(s): <br>
0.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
