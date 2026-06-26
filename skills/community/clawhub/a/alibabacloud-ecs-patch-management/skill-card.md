## Description: <br>
Scans and installs operating system patches on Alibaba Cloud ECS instances through OOS Operation Orchestration Service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdk-team](https://clawhub.ai/user/sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Cloud operations engineers and administrators use this skill to scan ECS instances for missing operating system patches, submit OOS patch executions, monitor execution status, inspect logs, and verify patch results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate real ECS patch installs that may change packages, create snapshots, or reboot instances. <br>
Mitigation: Confirm the exact region, instance IDs, action, reboot setting, snapshot setting, and retention window, and run installs only during an approved maintenance window. <br>
Risk: Alibaba Cloud credentials or overbroad RAM permissions could expose more infrastructure than the patch task requires. <br>
Mitigation: Use short-lived credentials or a least-privilege RAM role limited to the required OOS, ECS, snapshot, and patch-baseline actions. <br>
Risk: Unverified CLI installation or plugin setup could introduce supply-chain or tooling risk. <br>
Mitigation: Verify the Aliyun CLI installer and update CLI plugins before relying on the generated commands. <br>
Risk: Retries of patch execution requests could create duplicate executions, snapshots, or reboots. <br>
Mitigation: Use a deterministic ClientToken for OOS StartExecution and reuse the same token for retries with identical inputs. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sdk-team/alibabacloud-ecs-patch-management) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [RAM Policies](references/ram-policies.md) <br>
- [Related Commands](references/related-commands.md) <br>
- [Verification Methods](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [OOS Official Documentation](https://help.aliyun.com/zh/oos/) <br>
- [ACS-ECS-BulkyApplyPatchBaseline Template](https://help.aliyun.com/zh/oos/user-guide/acs-ecs-bulkyapplypatchbaseline) <br>
- [Patch Management Overview](https://help.aliyun.com/zh/oos/user-guide/patch-management) <br>
- [Cloud Assistant](https://help.aliyun.com/zh/ecs/user-guide/cloud-assistant-overview) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-confirmed region, instance IDs, patch action, reboot setting, snapshot setting, and snapshot retention before running cloud commands.] <br>

## Skill Version(s): <br>
0.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
