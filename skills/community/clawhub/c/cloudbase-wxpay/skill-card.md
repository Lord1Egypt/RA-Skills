## Description:

This skill provides battle-tested guidance for integrating WeChat Mini Program payment and refund flows using Tencent CloudBase, including unified orders, refunds, cloud functions, CLI deployment, and common failure fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jianqiaochen](https://clawhub.ai/user/jianqiaochen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, debug, and review CloudBase-backed WeChat Mini Program payment and refund integrations. It is especially relevant when payments fall back to simulated mode, refund status is ambiguous, cloud-call access tokens fail, or historical orders need refund backfill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Client-triggered forced refunds can bypass normal authorization and eligibility checks if copied into a public Mini Program path.

Mitigation: Restrict refund recovery to explicit admin or operator authorization, verify order ownership or eligibility, use idempotency and audit logging, and remove temporary public UI paths after backfill.

Risk: Payment and refund testing can silently use the wrong CloudBase or WeChat Pay environment.

Mitigation: Confirm sandbox or production environment selection, hardcode or explicitly configure the intended CloudBase environment ID, and validate required merchant environment variables before executing payment calls.

## Reference(s):

- [CloudBase WeChat Pay Pitfalls](references/gotchas.md)
- [ClawHub Skill Page](https://clawhub.ai/jianqiaochen/skills/cloudbase-wxpay)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline JavaScript, JSON, WXML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes deployment checklists, troubleshooting steps, and refund recovery guidance.]

## Skill Version(s):

3.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
