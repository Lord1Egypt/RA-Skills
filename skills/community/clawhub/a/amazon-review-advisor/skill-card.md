## Description: <br>
Amazon Review Advisor helps Amazon sellers classify review sentiment, prepare compliant review responses, identify abnormal review patterns, and turn customer feedback into product and operations improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Amazon sellers and ecommerce operators use this skill to analyze pasted Amazon review text, classify complaint themes and severity, draft policy-aware responses, and prioritize product, listing, logistics, or customer-service improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review response or review-request wording may become inconsistent with current Amazon policy. <br>
Mitigation: Verify Amazon's current review and buyer-contact policies before using public responses, appeal language, or review-request text. <br>
Risk: Seller-provided review examples may contain unnecessary buyer personal data. <br>
Mitigation: Paste only the minimum review and order context needed for analysis, and remove buyer personal data where it is not required. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/amazon-review-advisor) <br>
- [Publisher Profile](https://clawhub.ai/user/wangm-a3) <br>
- [Response Templates](references/response-templates.md) <br>
- [Amazon Seller Central](https://sellercentral.amazon.com) <br>
- [Review Reporting Guidelines](https://www.amazon.com/gp/help/customer/html.html?plattr=FOOT) <br>
- [Request a Review Feature](https://sellercentral.amazon.com/learn/courses?moduleId=8eb9f36c&quizId=34b&readId=a5e5c43a) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown guidance, response templates, review-health reports, and optional JSON from the analyzer script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include bilingual Chinese and English response text, sentiment labels, severity labels, complaint-theme summaries, and action recommendations.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
