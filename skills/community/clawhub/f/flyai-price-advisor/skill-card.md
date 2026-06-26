## Description: <br>
历史价格参谋 helps users decide whether to book now or wait by checking current flight and hotel prices, comparing nearby dates, estimating price level and trend, and returning a clear buy-or-wait recommendation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hello-ahang](https://clawhub.ai/user/hello-ahang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and travel-planning agents use this skill to evaluate whether a quoted flight or hotel price is favorable, compare nearby dates, and receive a booking recommendation with confidence and rationale. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow asks the agent to install or upgrade a global FlyAI CLI package, and its fallback mentions sudo. <br>
Mitigation: Review the FlyAI CLI source and package before installation, avoid sudo where possible, and prefer a user-scoped Node environment such as nvm. <br>
Risk: The workflow includes a NODE_TLS_REJECT_UNAUTHORIZED=0 workaround for certificate errors. <br>
Mitigation: Do not bypass TLS verification; fix certificate or network issues before running FlyAI commands. <br>
Risk: Personalization may store travel preferences in memory or ~/.flyai/user-profile.md. <br>
Mitigation: Ask before saving preferences and periodically review, edit, or delete stored travel profile data. <br>
Risk: Travel price predictions and booking recommendations can be wrong or become stale. <br>
Mitigation: Show confidence and uncertainty, verify live prices before purchase, and avoid presenting predictions as guarantees. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hello-ahang/flyai-price-advisor) <br>
- [Workflow](reference/workflow.md) <br>
- [User profile storage](reference/user-profile-storage.md) <br>
- [Flight search reference](reference/search-flight.md) <br>
- [Hotel search reference](reference/search-hotel.md) <br>
- [Examples](reference/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with price analysis, confidence labels, FlyAI command usage, and booking links when available] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current prices, nearby-date comparisons, buy-or-wait recommendations, confidence estimates, and user-profile preference handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
