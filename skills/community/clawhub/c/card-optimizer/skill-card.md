## Description: <br>
Credit card rewards optimizer that helps maximize cashback, points, and miles by recommending the best card for purchase categories, tracking annual caps, calculating annual fee ROI, managing rotating quarterly categories, and suggesting new cards from spending patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ScotTFO](https://clawhub.ai/user/ScotTFO) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to maintain a local credit card rewards profile, ask which card to use for a purchase category, analyze annual fee ROI, manage rotating quarterly categories, and identify rewards coverage gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local cards.json profile could expose sensitive financial information if users store more than card names, reward rules, and rough spending estimates. <br>
Mitigation: Keep cards.json limited to card names, reward rules, category mappings, activation status, and approximate spending estimates; do not store card numbers, bank logins, statements, credentials, or other secrets. <br>
Risk: Rewards rates, annual fees, bonus categories, and issuer terms can change, so generated recommendations may become outdated. <br>
Mitigation: Verify current issuer terms before relying on recommendations, especially when adding a new card, evaluating annual fee ROI, or changing card usage. <br>
Risk: Quarterly activation reminders are useful only when the user understands where they are configured and how to stop them. <br>
Mitigation: Enable quarterly reminders only in a known local scheduling mechanism and document how to disable or change them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ScotTFO/card-optimizer) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with optional JSON snippets for local cards.json updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local card definitions, reward rules, activation status, and rough spending estimates; it does not track individual purchases.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
