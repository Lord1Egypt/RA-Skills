## Description: <br>
Exports Alibaba Cloud WAF 3.0 configuration, including onboarding resources, defense policies, template bindings, account topology, and raw API payloads, into a multi-sheet Excel workbook for backup, audit, disaster recovery, and migration inventory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud security, platform, and operations engineers use this skill to create read-only WAF 3.0 configuration snapshots for audit, disaster recovery, migration planning, and periodic change tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled Python script runs dynamically built shell commands while using cloud credentials. <br>
Mitigation: Review the script before use, run it in an isolated environment, and prefer read-only RAM users or short-lived credentials. <br>
Risk: The generated workbook contains detailed WAF rules, protected assets, account topology, and raw configuration JSON. <br>
Mitigation: Store and share the workbook as sensitive security material with access controls appropriate for production configuration exports. <br>
Risk: Passing secrets through command-line arguments or chat could expose credentials. <br>
Mitigation: Configure credentials outside the agent session and avoid entering access keys or secrets in command-line arguments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-waf-config-backup) <br>
- [Publisher profile](https://clawhub.ai/user/sdk-team) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [Alibaba Cloud WAF OpenAPI overview](https://help.aliyun.com/zh/waf/web-application-firewall-3-0/developer-reference/api-waf-openapi-2021-10-01-overview) <br>
- [Alibaba Cloud WAF 3.0 documentation](https://www.alibabacloud.com/help/en/waf/web-application-firewall-3-0/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and a generated Excel workbook path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The generated workbook can contain sensitive WAF rules, protected assets, account topology, and raw configuration JSON.] <br>

## Skill Version(s): <br>
0.0.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
