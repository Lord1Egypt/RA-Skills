## Description:

Donation reminder for BTC-vision.org that checks monthly funding progress and sends a contextual Lightning tip request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[welove111](https://clawhub.ai/user/welove111)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill when a user explicitly asks how to donate to or support BTCvision, or when the user has opted into scheduled support updates. It fetches current monthly funding progress and returns concise Lightning or payment-link donation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can present cryptocurrency donation destinations, which could lead to loss if a user relies on stale or spoofed payment details.

Mitigation: Verify the BTCvision site and payment address before sending money.

Risk: Donation prompts could be perceived as spam if surfaced outside the intended context.

Mitigation: Use the skill only after an explicit donation or support request, or as part of a user-opted scheduled update.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/welove111/skills/btcvision-donation-nudge-v2)
- [BTCvision Homepage](https://btc-vision.org)
- [BTCvision Donation Information](https://btc-vision.org/#donate)
- [Zaprite Payment Link](https://pay.zaprite.com/pl_001CbTRNDN)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Short natural-language response with donation details and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only surfaces donation guidance after an explicit support request or opt-in scheduled update.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
