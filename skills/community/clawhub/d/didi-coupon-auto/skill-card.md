## Description:

自动领取滴滴出行优惠券，每天0点领取打车券包，并支持网约车、顺风车、代驾等多种出行券。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ayue-oss](https://clawhub.ai/user/ayue-oss)

### License/Terms of Use:

MIT-0

## Use Case:

External users with an OpenClaw browser session use this skill to open Didi's coupon page, claim available ride and travel coupons, and receive grouped coupon details. It can also be configured for daily scheduled coupon claiming.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill controls a logged-in Didi browser session to claim coupons automatically.

Mitigation: Run it only in a browser profile intended for this task, review the trigger phrases, and avoid unrelated browser tabs during execution.

Risk: Recurring automation may claim coupons daily without an interactive confirmation step.

Mitigation: Enable the daily schedule only after reviewing the cron configuration and disable or adjust it when automatic claiming is no longer desired.

Risk: The script writes daily claim logs that may include coupon and account-session context.

Mitigation: Review log contents and retention, and keep the skill workspace access limited to trusted users.

Risk: The WebSocket dependency can fall back outside the workspace if the expected package path is unavailable.

Mitigation: Prefer a package-local, locked ws dependency before routine use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ayue-oss/skills/didi-coupon-auto)
- [Didi coupon claim page](https://vv.didi.cn/a8ZdG0j?source_id=88446DIDI88446tkmmchild1001&ref_from=dunion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell and JSON snippets, plus plain-text coupon summaries and JSON claim logs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an OpenClaw browser exposed on CDP port 18800; writes daily claim logs under the skill logs directory.]

## Skill Version(s):

2.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
