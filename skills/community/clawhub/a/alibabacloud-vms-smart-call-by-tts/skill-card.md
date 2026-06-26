## Description: <br>
Alicloud VMS Smart Voice Call initiates AI-powered outbound voice calls from natural-language intent, matches a recipient from an address book, and can query call details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to place single-recipient Alibaba Cloud VMS smart voice notifications from a stated intent, then optionally query whether the call was accepted or answered. It assumes the user has configured Alibaba Cloud credentials, RAM permissions, and an address book outside the skill flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real AI-generated outbound calls and the security evidence notes that it may do so without a final confirmation. <br>
Mitigation: Require explicit final user confirmation before every call and limit use to lawful notification scenarios. <br>
Risk: The skill requires sensitive Alibaba Cloud credentials and billable cloud access. <br>
Mitigation: Use a least-privilege RAM user limited to dyvms:SubmitIntent and dyvms:QueryCallDetailByCallId; avoid root or broad cloud credentials. <br>
Risk: The installer and plugin workflow can make persistent local CLI changes, including shell startup PATH edits or plugin replacement. <br>
Mitigation: Review the installer before execution and confirm plugin source/path choices before allowing CLI plugin replacement. <br>


## Reference(s): <br>
- [Aliyun CLI Installation Guide](references/cli-installation-guide.md) <br>
- [External Network Fallback](references/external-network-fallback.md) <br>
- [Plugin Troubleshooting](references/plugin-troubleshooting.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance, API calls] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a single-recipient call initiation workflow and optional call-detail query; requires Alibaba Cloud credentials and should not print credential values.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
