## Description:

Provides 12306 rail-travel information retrieval and workflow assistance for ticket availability, waitlist status, and order summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to help with personal, compliant 12306 railway workflows such as checking ticket availability, monitoring waitlist status, and summarizing orders. It is intended for user-directed assistance and does not support captcha bypass, unofficial purchasing channels, scraping attacks, or bulk ordering.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may handle login sessions, passenger names, ID tail numbers, and order status.

Mitigation: Keep actions user-directed and avoid storing or sharing more personal travel data than needed.

Risk: Automated 12306 activity can trigger platform controls or violate service rules if used for captcha bypass, scraping, attacks, or bulk ordering.

Mitigation: Use the skill only for compliant official workflows, respect human verification, and apply conservative query limits.

## Reference(s):

- [12306 Official Site](https://www.12306.cn/)
- [12306 Ticket Booking](https://kyfw.12306.cn/otn/leftTicket/init)
- [12306 Waitlist Booking](https://kyfw.12306.cn/otn/subscribe)
- [ClawHub Skill Page](https://clawhub.ai/codekungfu/skills/12306-hot-trend)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or structured text summaries with optional CSV export guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ticket availability lists, waitlist status summaries, order summaries, reminders, and privacy-preserving travel data extracts.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
