## Description:

CouponClaw finds coupons, stacks cashback, and calculates the exact final price before checkout across China, the US, the UK, Australia, and Southeast Asia.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use CouponClaw to find currently valid coupon codes, compare cashback rates, and prepare final-price savings summaries for products, stores, and daily deals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coupon or cashback recommendations may be stale, unavailable, expired, or incompatible with cashback portal rules.

Mitigation: Review live merchant, coupon, and cashback pages before checkout and do not fabricate coupon codes when a page cannot be accessed.

Risk: The optional daily deals push can create a recurring scheduled notification until the user disables it.

Mitigation: Enable push only after reviewing the command, channel, region, language, and morning time; disable it with the provided push-toggle off command when no longer wanted.

## Reference(s):

- [CouponClaw on ClawHub](https://clawhub.ai/jiajiaoy/skills/couponclaw)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with source links, coupon and cashback tables, shell command examples, and optional cron protocol messages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Chinese output unless --lang en is passed; optional daily deal push uses a user-enabled recurring cron subscription.]

## Skill Version(s):

1.1.8 (source: server release metadata, package.json, _meta.json, and SKILL.md footer)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
