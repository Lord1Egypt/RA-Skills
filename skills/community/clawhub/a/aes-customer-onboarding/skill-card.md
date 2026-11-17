## Description:

Design post-first-purchase onboarding sequences that educate customers, reduce returns, and drive repeat orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce, lifecycle marketing, and customer experience teams use this skill to plan post-first-purchase onboarding sequences across email, SMS, push, and in-package touchpoints. It helps convert product, customer, delivery, and channel context into a structured onboarding playbook with timing, content direction, measurement, and testing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Planned SMS, push, or email campaigns may be launched without valid customer consent, opt-out handling, quiet-hour controls, or local privacy compliance.

Mitigation: Before launch, verify consent records, include opt-out paths, respect local quiet-hour and privacy laws, and preserve customer language preferences where practical.

Risk: Automated onboarding messages may continue after a return, support complaint, unsubscribe, spam complaint, second purchase, or review completion.

Mitigation: Apply suppression rules before activating the sequence, including pausing after support tickets, stopping non-transactional messages after unsubscribe or spam complaints, and suppressing irrelevant review or cross-sell requests.

Risk: Generic or incorrectly timed onboarding content may mislead customers, increase returns, or produce poor campaign performance.

Mitigation: Tie messages to confirmed delivery and customer milestones, segment by product and customer context, validate dynamic fields and links, and review metrics after launch.

## Reference(s):

- [Customer Onboarding Skill Page](https://clawhub.ai/leooooooow/skills/aes-customer-onboarding)
- [Output Template](references/output-template.md)
- [Onboarding Sequence Design Guide](references/onboarding-sequence-guide.md)
- [Channel Timing Reference Card](references/channel-timing-reference.md)
- [Customer Onboarding Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration]

**Output Format:** [Markdown playbooks, tables, checklists, and implementation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include customer communication timelines, channel assignments, content briefs, KPI definitions, A/B testing roadmaps, suppression rules, and compliance reminders.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
