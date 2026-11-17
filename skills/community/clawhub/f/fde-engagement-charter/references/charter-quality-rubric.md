# POC contract quality score

| Dimensions | 0 points | 1 point | 2 points |
|---|---|---|---|
| Decision-making problem | "Make a demo" | Goal but not specific | It is clear which decision to change after the end |
| Success criteria | Subjective evaluation | Indicators but no metric definition | Complete baseline, threshold, evidence, and owner |
| Scope | Feature list | Scope but fuzzy boundaries | Minimal workflow, non-target, extrapolation restrictions clear |
| Customer input | Verbal support | Contact person | People, data, access and time commitment |
| Data preparation | "Customer provided" | There are samples but no responsibility | Source, authority, quality, version and owner |
| User participation | Not scheduled | Proxy user | Real users, frequency and feedback method clear |
| Risk Governance | Not mentioned | General inspection | Hard access, approval, suspension and escalation clear |
| Change control | Requirements can be added at any time | Time box | Complete change impact, approval and version mechanisms |
| Failure handling | Only success is defined | There is a word stop | Failure, adjustment, stop and review actions are clear |
| PRD ready | Guessing still required | Partially writable | Specifications and acceptance can be written directly downstream |

Only if the score is 16 or above and the data, customer input, and risk management are not 0, it can be frozen.

## Review Questions

- What exactly will the customer approve if the technology demo is successful?
- Who sets each threshold? Why isn’t it set to make it easier to pass?
- Which indicators are hard gated and which can be weighed?
- Does a POC still have meaning when the customer does not provide a certain commitment?
- What scenarios are explicitly excluded to prevent temporary expansion of live demonstrations?
- Can failure lead to effective learning, rather than indefinite postponement?
