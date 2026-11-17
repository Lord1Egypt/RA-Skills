## Description:

GEO 周期自动协同 — 读龙虾密钥，自动导出范文/执行深度仿写并导出，上报待群发状态。供 QClaw 每日定时任务加载，无需用户说「开始优化任务」。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chameleon-nexus](https://clawhub.ai/user/chameleon-nexus)

### License/Terms of Use:

MIT-0

## Use Case:

External ClawHub users with a GEO SaaS account use this skill to run scheduled QClaw automation that verifies a local GEO API key, fetches optimization tasks, exports fanwen and fangxie ZIP files, and reports mass-publish readiness.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext local API key storage can expose the GEO account credential to other local processes or users.

Mitigation: Use a secure secret store or owner-only permissions for the key file before scheduled use.

Risk: Daily unattended authenticated actions may export files or update publish readiness based on remote service state without interactive review.

Mitigation: Install only for trusted GEO SaaS accounts and review exported ZIP files and status updates before downstream publishing.

Risk: Remote-controlled fetch and export paths can broaden data exposure or write unexpected local paths.

Mitigation: Restrict web_fetch to trusted public HTTPS URLs and validate path components such as brand, product, and cycle before writing exports.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chameleon-nexus/skills/geo-cycle-autopilot)
- [GEO SaaS service endpoint](https://ai.gaobobo.cn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, API call patterns, local file paths, and concise status summaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local ZIP export paths and human-facing status summaries; it should not expose internal optimization task IDs.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
