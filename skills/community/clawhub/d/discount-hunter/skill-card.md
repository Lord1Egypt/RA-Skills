## Description: <br>
Discount Hunter finds promo codes for the current checkout or cart page, tests them in the promo field, and avoids completing purchases. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetjellyfish](https://clawhub.ai/user/puppetjellyfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill on checkout or cart pages to search for discount codes, apply only promo-code controls, and report whether any code reduces the order total. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill opens third-party coupon and search pages using the store name or domain from the checkout page. <br>
Mitigation: Install only if this disclosure is acceptable, and avoid using the skill on pages where the merchant name or domain should not be shared with coupon or search sites. <br>
Risk: The skill operates on checkout pages where an accidental purchase action would have financial impact. <br>
Mitigation: Monitor the checkout page while it runs and confirm it only applies promo codes, never clicks Pay, Place Order, Submit Payment, or similar purchase controls. <br>


## Reference(s): <br>
- [Discount Hunter on ClawHub](https://clawhub.ai/puppetjellyfish/discount-hunter) <br>
- [Publisher profile: puppetjellyfish](https://clawhub.ai/user/puppetjellyfish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown status updates and summary tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports detected promo codes, attempted results, successful savings when visible, and safety stop conditions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
