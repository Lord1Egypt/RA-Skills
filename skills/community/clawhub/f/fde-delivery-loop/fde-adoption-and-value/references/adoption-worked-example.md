# Full example of adoption and value

## Pilot scope

20 billing agents, observed for 4 weeks. Qualified usage events are defined as "Complete a real ticket draft and submit it for manual review" and are not counted as logins.

## Use funnels

| Stage | Number of people | Discovery |
|---|---:|---|
| Gain access | 20 | Complete training |
| First success | 18 | 2 people failed to configure permissions |
| Reuse in second week | 15 | 3 people think it’s faster to write simple tickets by hand |
| Fourth week of continued use | 14 | 1 person distrusts policy freshness |
| Workflow dependencies | 11 | Mainly focused on complex bill interpretation |

## Mission and Value

- Median processing time dropped from 11.5 minutes to 7.4 minutes, a decrease of 35.7%;
- Rework due to the old policy dropped from 18% to 4%;
- Manual review adds an average of 1.2 minutes, which is already included in the processing time;
- API, infrastructure, support and content maintenance total 0.42 yuan per ticket;
- Customer service executive confirms quality improvements, but finance has not yet confirmed monetized ROI.

## Attribution Limitations

The policy library was also cleaned up during the same period, so the drop in rework cannot be entirely attributed to the agent. Peak adoption has FDE on-site support, long-term support costs remain to be proven.

## Decision

Conditionally expand to a second 20-person team, which only covers complex bill explanations; first fix permission activation, self-service troubleshooting, and policy freshness prompts. Simple ticket are not promoted for the time being because the net time gain is insufficient.

## Candidate for productization

- Versioning policy retrieval and source display;
- Read-only CRM context connector;
- Customer service draft evaluation set;
- High-risk action mode of "use after manual confirmation".
