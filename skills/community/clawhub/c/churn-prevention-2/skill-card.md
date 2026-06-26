## Description: <br>
Helps agents advise on SaaS churn reduction through cancellation flows, save offers, failed-payment recovery, retention strategies, exit surveys, and win-back planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mrhuang09](https://clawhub.ai/user/Mrhuang09) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Product, growth, customer success, and engineering teams use this skill to design retention programs for subscription products. It supports voluntary churn reduction with cancel flows and save offers, and involuntary churn reduction with dunning and payment-recovery guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cancellation-flow guidance could be used to hide, block, or delay cancellation, especially for high-value accounts. <br>
Mitigation: Keep cancellation customer-controlled and clearly available, and get legal review before implementing any flow that changes self-service cancellation access. <br>
Risk: Product-marketing context, churn metrics, or customer examples used to tailor recommendations may contain sensitive business or customer information. <br>
Mitigation: Remove secrets and unnecessary sensitive data from local context before using the skill, and review generated recommendations before production use. <br>


## Reference(s): <br>
- [Cancel Flow Patterns](references/cancel-flow-patterns.md) <br>
- [Dunning Playbook](references/dunning-playbook.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Configuration] <br>
**Output Format:** [Markdown guidance with tables, templates, flow outlines, and implementation recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May tailor recommendations using local product-marketing context when available.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact metadata version 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
