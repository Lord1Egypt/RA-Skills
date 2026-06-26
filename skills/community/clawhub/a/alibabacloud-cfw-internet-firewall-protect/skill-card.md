## Description: <br>
Manage Alibaba Cloud Cloud Firewall (CFW) Internet Firewall public IP protection switches, including status queries, enable and disable operations, bulk protection, auto-protection settings, and member-account targeting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations and security engineers use this skill to inspect and manage Alibaba Cloud CFW Internet Firewall protection for public IP assets, including targeted changes, bulk account-level operations, and auto-protection configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A narrow request may broaden into account-wide firewall changes, including enable-all, disable-all, or broader filters after a failed name or tag search. <br>
Mitigation: Review every proposed firewall change before execution, require explicit approval for the exact scope, and do not use enable-all, disable-all, or broader fallback scopes unless the operator requested them. <br>
Risk: Overbroad RAM permissions can allow wide changes to public IP firewall protection. <br>
Mitigation: Use least-privilege RAM permissions and reserve all-public-IP switch permissions for operators who truly need account-wide changes. <br>


## Reference(s): <br>
- [Resource Types](references/resource-types.md) <br>
- [RAM Permission List](references/ram-policies.md) <br>
- [CFW API Error Codes](references/api-errors.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Text] <br>
**Output Format:** [Markdown with inline bash commands and JSON command output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include impact previews, confirmation prompts, dry-run commands, and status verification summaries.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
