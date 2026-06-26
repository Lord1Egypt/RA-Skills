## Description: <br>
Search and shop on Amazon.com through buystuff.ai, compare products, manage a cart, and request a user-approved payment link for orders shipped to US addresses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasgeeksinthewood](https://clawhub.ai/user/lucasgeeksinthewood) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and AI agents use this skill to search Amazon products, compare options, build a cart, collect shipping and email details, and send a payment link for manual user approval. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product searches, cart details, shipping address, and email to buystuff.ai as an intermediary for Amazon purchases. <br>
Mitigation: Install only if that data sharing is acceptable, and disclose the intermediary before collecting shipping or email details. <br>
Risk: A payment link can be requested for a cart even though the API itself does not charge money. <br>
Mitigation: Before requesting the payment link, confirm the exact products, total price, 10% service fee, shipping address, recipient, and email with the user. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/lucasgeeksinthewood/buy-amazon) <br>
- [buystuff.ai](https://buystuff.ai) <br>
- [Rainforest API](https://www.rainforestapi.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown with API request examples and user-facing order summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires preserving the session ID across related cart and checkout calls.] <br>

## Skill Version(s): <br>
1.2.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
