## Description:

购买麦当劳商品的技能，通过claw_pay接口实现余额支付。仅适用于中国地区。Invoke when user wants to buy McDonald's products using claw wallet balance in China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vikky-lin](https://clawhub.ai/user/vikky-lin)

### License/Terms of Use:

MIT-0

## Use Case:

External users in China use this skill to check claw wallet balance, view available McDonald's items, purchase items through the claw_pay service, and receive a redemption link for in-store pickup or dine-in redemption.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can initiate real purchases through a third-party claw_pay service.

Mitigation: Confirm the item, price, wallet identity, and user intent before any purchase request.

Risk: The access_token functions like a wallet credential and may be exposed through URLs or logs.

Mitigation: Treat the token as secret, avoid sharing it in prompts or logs, and prefer versions that redact tokens from request paths and error output.

Risk: The payment service, revocation, and dispute process are insufficiently disclosed in the provided evidence.

Mitigation: Install only after trusting the service operator and documenting how users can revoke credentials or dispute failed purchases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vikky-lin/skills/buy-mcdonald)
- [Publisher profile](https://clawhub.ai/user/vikky-lin)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON-like API responses and concise user-facing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet balance, product listings, purchase status, payment time, and a McDonald's redemption link.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
