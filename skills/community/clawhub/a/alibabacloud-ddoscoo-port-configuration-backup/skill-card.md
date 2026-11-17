## Description:

Export, import, and restore Alibaba Cloud DDoS Pro manual non-website TCP and UDP port forwarding rules and their portable configuration through Aliyun CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud operations engineers and security teams use this skill to back up, migrate, reuse, and restore manual non-website Alibaba Cloud DDoS Pro TCP and UDP port forwarding configurations. It is intended for configuration portability and recovery, not website-derived rules, infrastructure protection, or runtime traffic and attack data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Import can change live DDoS Pro port forwarding and security policy, including deleting and recreating manual rules.

Mitigation: Use a least-privilege Aliyun profile, confirm the exact target instance and EIP before import, require exact readback verification, and revoke temporary write permissions after restore.

Risk: An export or import could act on the wrong scope if profile, region, resource group, instance, EIP, protocol, or port identity is assumed.

Mitigation: Require explicit parameter confirmation before cloud API calls and operate only on confirmed manual non-website TCP or UDP ports.

Risk: Credential or profile details could be exposed if they are read, printed, or saved in artifacts.

Mitigation: Use only existing Aliyun CLI profiles selected by the user and never read, display, or persist AccessKeys, tokens, profile names, signed URLs, or request headers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sdk-team/skills/alibabacloud-ddoscoo-port-configuration-backup)
- [Publisher profile](https://clawhub.ai/user/sdk-team)
- [Export workflow](references/export-workflow.md)
- [Import workflow](references/import-workflow.md)
- [Verification method](references/verification-method.md)
- [One-port YAML schema](references/schema.md)
- [Coverage matrix](references/coverage-matrix.md)
- [Least-privilege RAM policies](references/ram-policies.md)
- [Verified Aliyun CLI commands](references/related-commands.md)
- [Aliyun CLI installation and profile checks](references/cli-installation-guide.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline bash commands and one-port YAML backup files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Export writes one YAML file per manual port; import reports item-by-item restoration status after exact readback verification.]

## Skill Version(s):

0.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
