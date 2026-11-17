## Description:

Manage Alibaba Cloud Lingjun regular-node and hyper-node lifecycle operations, including stop, reboot, reimage, renewal, spec changes, repair, run-command, node-group default updates, tagging, and resource-group changes with required inventory and confirmation gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers use this skill to plan and execute post-provisioning operations on Alibaba Cloud Lingjun nodes while preserving confirmation, permission, region, and verification checks.

### Deployment Geography for Use:

Alibaba Cloud Lingjun supported regions, including cn-wulanchabu, cn-shanghai, cn-beijing, cn-hangzhou, the cn-wulanchabu-test-6 test region, and international gateways.

## Known Risks and Mitigations:

Risk: The skill can guide infrastructure mutations that stop, reboot, reimage, renew, change node specs, run commands, update node-group defaults, tag resources, or move resource groups.

Mitigation: Use read-only inventory first, match endpoint to region, require explicit single-step confirmation, and verify cloud-side state before reporting completion.

Risk: Reimage and renewal flows can cause data loss or paid irreversible orders.

Mitigation: Show a danger notice and confirmation table, require the exact confirmation word, and never infer ImageId or RenewPeriod.

Risk: Run-command and credential setup can expose secrets or execute unsafe shell content.

Mitigation: Redact access keys, passwords, and secret command parameters; prefer parameterized commands and least-privilege RAM policies.

Risk: The security review flags installation and safety-wrapper review risk.

Mitigation: Install only in a controlled Alibaba Cloud operations environment with a verified, pinned Alibaba Cloud CLI and plugins before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-lingjun-node-ops)
- [CLI installation guide](references/cli-installation-guide.md)
- [Endpoint routing](references/endpoint-routing.md)
- [Parameter confirmation](references/parameter-confirmation.md)
- [RAM policies](references/ram-policies.md)
- [Node power operations](references/node-power-operations.md)
- [Node renewal](references/node-renew.md)
- [Node spec change](references/node-spec-change.md)
- [Node repair](references/node-repair.md)
- [Node exec command](references/node-exec-command.md)
- [Node group update](references/node-group-update.md)
- [Tag and resource group](references/tag-and-resource-group.md)
- [Alibaba Cloud RAM console](https://ram.console.aliyun.com/manage/ak)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with confirmation tables, inline shell commands, receipts, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive values such as access keys and passwords are redacted in user-facing output.]

## Skill Version(s):

0.0.1 (source: server release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
