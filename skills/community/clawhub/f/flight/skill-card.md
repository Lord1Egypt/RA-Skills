## Description: <br>
Search, compare, book, and manage flights with price tracking, multi-platform comparison, and loyalty optimization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and travel-planning agents use this skill to compare flight options, track prices and status, manage booking decisions, and optimize loyalty points while keeping high-impact travel actions subject to user approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent could proceed with booking, payment, cancellation, or rebooking without sufficiently clear user approval. <br>
Mitigation: Require explicit user confirmation before any booking, payment, cancellation, rebooking, or non-refundable purchase action. <br>
Risk: Saved preferences, PNRs, travel history, and loyalty details may contain sensitive travel or account information. <br>
Mitigation: Keep loyalty credentials out of routine prompts, review saved travel files, and delete stored PNRs or history when no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/flight) <br>
- [Publisher Profile](https://clawhub.ai/user/ivangdavila) <br>
- [Search Guide](artifact/search.md) <br>
- [Booking Guide](artifact/booking.md) <br>
- [Price Tracking Guide](artifact/tracking.md) <br>
- [Miles, Points, and Loyalty Guide](artifact/points.md) <br>
- [APIs and Integrations Guide](artifact/apis.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration] <br>
**Output Format:** [Markdown guidance, checklists, comparisons, alerts, and suggested travel actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local preference, search, booking, alert, and travel-history files when the agent follows the skill instructions.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
