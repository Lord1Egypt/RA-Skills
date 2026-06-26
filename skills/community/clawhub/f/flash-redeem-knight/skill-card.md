## Description: <br>
Universal browser automation for prepaid H5 coupon redemption (food, beverage, pickup vouchers). Use when a user provides a prepaid redemption link and wants automatic store selection, option selection, final code extraction, and screenshot proof without extra payment risk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vshen009](https://clawhub.ai/user/vshen009) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to redeem already-paid H5 food, beverage, and pickup coupon links by selecting the intended store and options, confirming redemption, and extracting the final pickup or verification code with screenshot proof. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may consume a prepaid coupon or choose the wrong store or items if preferences or page state are misunderstood. <br>
Mitigation: Verify user authorization, store, item selections, and pickup mode before final confirmation, and pause when there is ambiguity. <br>
Risk: A redemption page may introduce unexpected extra payment or a non-prepaid checkout path. <br>
Mitigation: Confirm that the coupon is already paid and no extra payment is required before redeeming; stop and ask for confirmation if payment risk appears. <br>
Risk: Saved preferences may allow coupon consumption without fresh confirmation. <br>
Mitigation: Use persistent redemption preferences cautiously and require fresh confirmation for possible extra payment or material changes. <br>


## Reference(s): <br>
- [Coupon Redemption Profile Template](references/profile-template.md) <br>
- [ClawHub Release Page](https://clawhub.ai/vshen009/flash-redeem-knight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown receipt with redemption status, code, store, item summary, amount, and screenshot reference] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a final-page screenshot when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
