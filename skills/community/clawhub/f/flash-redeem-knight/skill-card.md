## Description:

Universal browser automation for prepaid H5 coupon redemption links that helps select stores and options, extract the final code, and provide screenshot proof without extra payment risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vshen009](https://clawhub.ai/user/vshen009)

### License/Terms of Use:


## Use Case:

Users with prepaid H5 coupon links use this skill to redeem eligible food, beverage, or pickup vouchers through browser automation, selecting the intended store and options and returning the final pickup or redemption code with proof. The workflow is intended for coupons the user is authorized to consume and stops for invalid, expired, already-used, or extra-payment states.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may redeem a prepaid coupon irreversibly or choose the wrong store or pickup option.

Mitigation: Confirm the user is authorized to consume the coupon and verify the intended store and pickup choices before final redemption.

Risk: A redemption page may request extra payment or show a state such as invalid, used, or expired.

Mitigation: Stop before any extra payment and report invalid, used, expired, or uncertain states instead of continuing by guesswork.

Risk: Redemption codes and screenshots can expose usable coupon information.

Mitigation: Treat final codes and screenshots as sensitive until the coupon has been used.

## Reference(s):

- [Coupon Redemption Profile Template](references/profile-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured Markdown receipt with redemption status, code, store, item summary, amount details, and screenshot reference when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser navigation guidance and final-page screenshot proof; redemption codes and screenshots should be treated as sensitive until used.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
