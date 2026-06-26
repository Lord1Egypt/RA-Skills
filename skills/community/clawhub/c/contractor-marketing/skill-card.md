## Description: <br>
AI marketing department for contractors and home service businesses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[blueprintstudioco](https://clawhub.ai/user/blueprintstudioco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External contractors and home service business operators use this skill to draft and organize marketing work across SEO, Google Business Profile, social media, advertising, proposals, review responses, lead follow-up, email, job costing, and competitor audits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Detailed business onboarding may collect sensitive operational data such as employee names, license numbers, payment methods, budgets, addresses, and marketing account status. <br>
Mitigation: Provide only the data needed for the current task and avoid sensitive business details unless storing them in workspace memory is acceptable. <br>
Risk: The skill uses an external strategy service for marketing context. <br>
Mitigation: Approve each external lookup and keep sensitive customer, employee, payment, or licensing details out of query terms. <br>
Risk: Recurring marketing automation and ad-budget guidance could publish content, contact customers, respond to reviews, or change spend without clear opt-in controls. <br>
Mitigation: Require explicit approval for every post, review reply, customer message, ad-budget change, scheduled task, and recurring automation. <br>
Risk: Draft proposals, review replies, and customer messages can affect customer relationships and business reputation. <br>
Mitigation: Use generated content as a draft and review accuracy, tone, pricing, scope, and legal terms before sending or publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/blueprintstudioco/contractor-marketing) <br>
- [Ad Creative Angles](references/ad-creative-angles.md) <br>
- [Business Profile Onboarding Questions](references/onboarding-questions.md) <br>
- [Proposal Template](references/proposal-template.md) <br>
- [Review Response Rules](references/review-response-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, plain text, HTML proposal drafts, shell commands, and structured tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store business profile answers in workspace memory and may suggest recurring marketing automation; review external lookups and scheduled actions before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
