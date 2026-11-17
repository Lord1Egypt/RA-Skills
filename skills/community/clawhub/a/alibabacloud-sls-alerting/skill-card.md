## Description:

Manage Alibaba Cloud SLS alerts and notifications. Use when configuring SLS alert rules, managing notification resources, or investigating alert events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sdk-team](https://clawhub.ai/user/sdk-team)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operators use this skill to configure Alibaba Cloud SLS alert rules, notification resources, alert policies, and content templates, and to investigate alert events using SLS history and diagnostic evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install guide includes a remote shell installer for Aliyun CLI before workflows that can affect cloud alerting resources.

Mitigation: Install Aliyun CLI only from a trusted and verified source, or inspect the installer before execution.

Risk: The skill can guide high-impact SLS alerting changes, including updates to rules, notification resources, policies, and mute state.

Mitigation: Use least-privilege RAM permissions, avoid delete permissions unless required, review dry-run output, and read back writes before relying on the change.

Risk: Using an unintended CLI profile could apply changes to the wrong Alibaba Cloud account or region.

Mitigation: Use the default profile unless a specific profile is intended, and verify project, region, and endpoint details before writes.

## Reference(s):

- [CLI installation guide](references/cli-installation-guide.md)
- [Manage alert rules](references/rules/manage-alert-rules.md)
- [Manage alert notifications](references/notifications/manage-notifications.md)
- [Alert event diagnosis](references/diagnosis/diagnose.md)
- [Region and endpoint configuration](references/regions.md)
- [Related APIs](references/related-apis.md)
- [RAM policies](references/ram-policies.md)
- [Skill usage troubleshooting](references/troubleshooting.md)
- [Official Aliyun CLI documentation](https://help.aliyun.com/zh/cli/)
- [Official CLI credential configuration documentation](https://help.aliyun.com/zh/cli/configure-credentials/)
- [Alert-log analysis guide](https://help.aliyun.com/zh/sls/use-custom-query-statements-to-analyze-alert-logs)
- [Alert rule evaluation log fields](https://help.aliyun.com/zh/sls/fields-in-alert-rule-evaluation-logs)
- [Alert resource data structure](https://help.aliyun.com/zh/sls/developer-reference/data-structure-of-alert-resource-data)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON configuration examples, and Python validation helpers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured Aliyun CLI credentials and adds a skill-specific user agent to cloud API calls.]

## Skill Version(s):

0.0.2 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
