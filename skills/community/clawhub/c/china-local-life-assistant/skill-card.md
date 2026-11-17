## Description:

China local-life flagship assistant for comparing food delivery, restaurant, ride, hotel, flight, train, and local service options across Meituan, Eleme, Dianping, Didi, Qunar, Trip.com, and related platforms by price, time, distance, ratings, coupons, and risk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare China local-life services and choose practical options for food delivery, restaurants, rides, travel, and nearby services. It helps surface tradeoffs, coupon caveats, merchant risk cues, and manual next actions without logging in, booking, ordering, or paying.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: Final prices, coupon terms, delivery times, availability, and merchant behavior may differ from the comparison output.

Mitigation: Manually review platform prices, availability, coupon terms, and merchant risk before acting.

Risk: The skill is used near account, booking, order, or payment flows for local services or travel.

Mitigation: Do not provide credentials, identity checks, addresses, payment details, or authorization codes, and keep all bookings, orders, confirmations, and payments manual.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, Analysis, Markdown]

**Output Format:** [Markdown text with comparison guidance and manual next actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not perform login, booking, order submission, or payment actions.]

## Skill Version(s):

1.1.0 (source: evidence.release.version and artifact/skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
