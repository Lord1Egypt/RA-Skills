## Description:

Order food from TGO Yemek (Trendyol GO), Turkey's leading food delivery service. Use when user wants to order food delivery in Turkey, browse restaurants, search for foods, manage delivery addresses, check order history, or checkout with 3D Secure payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rersozlu](https://clawhub.ai/user/rersozlu)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to browse TGO Yemek restaurants in Turkey, manage delivery addresses and carts, and complete food orders with 3D Secure payment. It is intended for real food ordering workflows, not merely menu lookup.

### Deployment Geography for Use:

Turkey

## Known Risks and Mitigations:

Risk: The skill handles Trendyol GO account credentials, saved addresses, cart contents, masked card metadata, and order placement.

Mitigation: Install only when the publisher is trusted for those actions, and require explicit user confirmation before address, cart, order note, or payment changes.

Risk: Credentials and JWTs may be exposed through shell-profile exports or local token cache files.

Mitigation: Prefer a dedicated secret manager, avoid displaying credentials or tokens, and clear cached tokens when the session is complete.

Risk: 3D Secure payment handling writes payment HTML to a temporary local file and opens it in a browser.

Mitigation: Review the browser handoff before use and remove temporary payment files after verification.

Risk: The optional Google Places API key can expand the data and credential exposure surface.

Mitigation: Omit or tightly restrict GOOGLE_PLACES_API_KEY unless Google Reviews are needed.

## Reference(s):

- [TGO Yemek API Quick Reference](references/api-quick-ref.md)
- [ClawHub Skill Page](https://clawhub.ai/rersozlu/skills/food402)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline Bash commands and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, openssl, TGO_EMAIL, and TGO_PASSWORD; GOOGLE_PLACES_API_KEY is optional for Google Reviews.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
