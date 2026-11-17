## Description:

Amazon Review Advisor helps Amazon sellers classify review sentiment, identify complaint themes, draft compliant review responses, and turn review trends into product and operations improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

Amazon sellers and ecommerce operators use this skill to analyze pasted product reviews, triage negative feedback, prepare compliant public or buyer-contact wording, and prioritize product, listing, logistics, and customer-service improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated buyer-contact, refund, or review-request wording could conflict with current Amazon Seller policies if used without review.

Mitigation: Verify all customer-facing wording against current Amazon policy and use Amazon's official Request a Review workflow for review invitations.

Risk: Review text or order details may contain unnecessary personal data.

Mitigation: Paste only the information needed for analysis and remove personal data that is not required for the response or appeal.

Risk: Operators could misuse templates to pressure or reward customers for changing reviews.

Mitigation: Do not offer compensation, refunds, or other benefits in exchange for modifying or deleting reviews.

## Reference(s):

- [Response Templates](artifact/references/response-templates.md)
- [Amazon Seller Central](https://sellercentral.amazon.com)
- [Review Reporting Guidelines](https://www.amazon.com/gp/help/customer/html.html?plattr=FOOT)
- [Request a Review Feature](https://sellercentral.amazon.com/learn/courses?moduleId=8eb9f36c&quizId=34b&readId=a5e5c43a)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown prose, tables, response templates, and optional JSON review-health reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-first guidance with English response templates; outputs may include sentiment labels, complaint themes, severity, appeal material checklists, and action recommendations.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
