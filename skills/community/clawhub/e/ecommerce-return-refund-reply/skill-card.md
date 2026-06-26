## Description: <br>
Generate standardized, policy-compliant customer service replies for e-commerce return, exchange, and refund inquiries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Customer service teams and commerce agents use this skill to draft ready-to-send buyer replies for return, exchange, refund, eligibility, damaged-item, wrong-item, size, quality, change-of-mind, and refund-status inquiries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated replies may contain internal notes or policy assumptions that should not be sent directly to a buyer. <br>
Mitigation: Review the full response before sending, especially the internal notes and policy details. <br>
Risk: Metadata tags include purchase and crypto capabilities even though the artifact is a markdown-only drafting helper. <br>
Mitigation: Install it for drafting customer-service responses only and avoid granting unnecessary purchase, payment, or crypto permissions. <br>
Risk: Refund or shipping promises can be inaccurate if the return window, fault determination, or refund stage is missing or wrong. <br>
Mitigation: Confirm order details, platform policy, return window, shipping responsibility, and refund status before using the generated reply. <br>


## Reference(s): <br>
- [Reply Templates by Issue Type](references/reply-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with a ready-to-send reply and internal notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Buyer-facing reply is intended to stay under 200 words and include issue type, template used, and policy checked notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
