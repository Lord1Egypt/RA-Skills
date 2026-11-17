## Description:

Helps agents query FlyWise for real-time flight prices, top itinerary details, 30-day route price history, and buy-now-or-wait guidance after an Alipay HTTP 402 payment flow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyuqiu2023](https://clawhub.ai/user/heyuqiu2023)

### License/Terms of Use:

MIT-0

## Use Case:

Students and travelers use this skill through an agent to compare flight prices for China-related routes, inspect leading itinerary options, and decide whether to book now or wait. It is most relevant for one-way student travel, return-to-school trips, and long-haul or regional routes described by the FlyWise service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Itinerary details are sent to flywise.win and payment is handled through a separate Alipay HTTP 402 flow.

Mitigation: Confirm the user is comfortable sharing route, date, cabin, and related itinerary details before contacting the service or initiating payment.

Risk: Payment response bodies and Payment-Proof credentials may be exposed too broadly if copied verbatim or logged with verbose curl output.

Mitigation: Avoid forwarding complete payment responses unless required, remove verbose credential-bearing output from user-visible logs, and treat Payment-Proof values as sensitive.

Risk: Returned recommendation text or detail links may influence purchase decisions or direct users to external pages.

Mitigation: Present recommendations as service-provided guidance, validate returned links before showing them, and encourage users to compare against other booking sources for important travel purchases.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heyuqiu2023/skills/flywise-flights)
- [FlyWise flight search](https://flywise.win/flights/search)
- [FlyWise paid flight API example](https://flywise.win/api/ai-pay/flights?from=PEK&to=SHA&date=2026-05-10&cabin=economy&max_results=3)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown guidance with curl commands and summarized JSON flight results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prices, airline and aircraft details, cabin, layovers, 30-day price comparisons, recommendation text, and returned detail links.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
