## Description:

优化飞书扩展的 probe 缓存配置，将健康检查缓存延长至成功 24 小时、失败 1 小时，以减少飞书 Bot API 调用次数。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bobbycats](https://clawhub.ai/user/bobbycats)

### License/Terms of Use:


## Use Case:

Developers and operators maintaining OpenClaw Feishu integrations use this skill to tune health-check cache durations and reduce repeated Feishu Bot API calls. It also helps them rebuild, restart, and verify the gateway after changing the probe configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broken or revoked Feishu integration may continue to look healthy for up to 24 hours after the success cache is extended.

Mitigation: Review the cache values before production use and perform manual service and integration checks after applying the change.

Risk: Restarting the OpenClaw gateway can briefly interrupt service.

Mitigation: Schedule the restart during an acceptable maintenance window and verify the gateway returns to active running status.

Risk: OpenClaw upgrades may overwrite the modified probe cache settings.

Mitigation: Reapply the probe.ts cache changes, run a full pnpm build, and restart the gateway after major OpenClaw updates.

Risk: Building only the Feishu extension can leave other extension artifacts missing and cause gateway startup failures.

Mitigation: Use the documented full build and confirm dist/extensions contains all expected extensions before restarting the service.

## Reference(s):

- [飞书 Bot API 文档](https://open.feishu.cn/document/server-docs/bot-v3/bot-info)
- [OpenClaw 飞书扩展](https://docs.openclaw.ai/channels/feishu)
- [ClawHub skill page](https://clawhub.ai/bobbycats/skills/feishu-probe-optimize)
- [ClawHub publisher profile](https://clawhub.ai/user/bobbycats)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash and TypeScript code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes cache-duration values, verification steps, and troubleshooting guidance for the OpenClaw Feishu extension.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
