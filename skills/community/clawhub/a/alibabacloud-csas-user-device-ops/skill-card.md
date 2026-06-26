## Description: <br>
Helps agents query Alibaba Cloud SASE users and devices, analyze inactive devices, and perform reversible device locking through Aliyun CSAS CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators and cloud administrators use this skill to inspect Alibaba Cloud SASE user and device state, investigate inactive endpoints, and lock inactive devices after preview and explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill operates against Alibaba Cloud SASE and may require sensitive cloud credentials. <br>
Mitigation: Use an existing Aliyun CLI profile, configure credentials outside the agent session, and avoid reading, echoing, or placing access-key secrets in commands. <br>
Risk: Broad CSAS permissions can allow device-state changes beyond read-only analysis. <br>
Mitigation: Prefer a least-privilege RAM policy and use read-only permissions unless device locking is specifically needed. <br>
Risk: Device locking changes endpoint access state, even though it is reversible. <br>
Mitigation: Run a dry-run preview, review the exact target devices, require explicit confirmation, and verify device status after the action. <br>
Risk: CLI validation and setup steps can change Aliyun CLI plugin behavior by enabling auto plugin install or updating plugins. <br>
Mitigation: Review setup commands before execution and run them in an approved environment where Aliyun CLI plugin updates are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/sdk-team/alibabacloud-csas-user-device-ops) <br>
- [Acceptance criteria](references/acceptance-criteria.md) <br>
- [SASE API reference](references/api-reference.md) <br>
- [Aliyun CLI installation guide](references/cli-installation-guide.md) <br>
- [RAM permission list](references/ram-policies.md) <br>
- [Related CLI commands](references/related-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, API Calls, JSON, Guidance] <br>
**Output Format:** [Markdown summaries with tables, inline shell commands, and structured JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Write operations are expected to use dry-run previews, explicit confirmation, and post-action verification.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
