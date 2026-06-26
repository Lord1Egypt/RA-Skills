## Description: <br>
Order food from TGO Yemek (Trendyol GO), Turkey's leading food delivery service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rersozlu](https://clawhub.ai/user/rersozlu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users in Turkey use this skill to browse nearby restaurants, compare menu items, manage delivery addresses, add food to a basket, and complete TGO Yemek checkout with 3D Secure payment. <br>

### Deployment Geography for Use: <br>
Turkey <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real food orders and interact with saved-card checkout flows. <br>
Mitigation: Confirm the restaurant, items, address, total, and payment card before checkout or 3D Secure verification. <br>
Risk: The skill uses account sessions and can access delivery addresses, cart contents, saved-card flow, and order history. <br>
Mitigation: Install only when this account access is acceptable, and avoid shared machines unless token storage is fixed. <br>
Risk: The optional Google Places integration requires a Google Places API key. <br>
Mitigation: Provide GOOGLE_PLACES_API_KEY only when restaurant review lookup is needed. <br>


## Reference(s): <br>
- [Food402 ClawHub Listing](https://clawhub.ai/rersozlu/food402) <br>
- [TGO Yemek API Quick Reference](artifact/references/api-quick-ref.md) <br>
- [TGO Yemek Website](https://tgoyemek.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON responses from TGO and payment API calls.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TGO_EMAIL and TGO_PASSWORD. GOOGLE_PLACES_API_KEY is optional for Google Reviews.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
