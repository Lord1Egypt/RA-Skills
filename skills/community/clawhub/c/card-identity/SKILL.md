---
name: card-identity
description: Resolve a card name to an exact issuer, family, and variant. Use internally before card research when shorthands, ambiguous names, or personal-versus-business variants appear.
---

# Card Identity

Resolve the user's input to one exact card variant before any research.

## Workflow

1. Normalize whitespace and common shorthands using the table below.
2. Split issuer, family, and variant when possible.
3. Check issuer support against [../card-shared/source-policy.yaml](../card-shared/source-policy.yaml). If the issuer is unsupported, return: `This card is not from a supported issuer.`
4. Apply ambiguity rules from [../card-shared/card-identity-rules.md](../card-shared/card-identity-rules.md).
5. When the match is confident, keep identity in the hidden YAML keys from [../card-shared/normalization-rules.md](../card-shared/normalization-rules.md). When it is not confident, stop and return a numbered choice list.

## Output Rules

- Do not merge facts across variants.
- If a personal and business version both fit and the user did not specify which one, return both and stop.
- If no plausible match exists, return: `Could not match a card. Try including the full card name with issuer.`

## Common Abbreviations

| Input | Resolved |
| --- | --- |
| CSP | Chase Sapphire Preferred |
| CSR | Chase Sapphire Reserve |
| CFU | Chase Freedom Unlimited |
| CFF | Chase Freedom Flex |
| CIP | Chase Ink Business Preferred |
| CIC | Chase Ink Business Cash |
| CIU | Chase Ink Business Unlimited |
| Amex Gold | American Express Gold Card |
| Amex Plat | American Express Platinum Card |
| Amex Biz Gold | American Express Business Gold Card |
| Amex Biz Plat | American Express Business Platinum Card |
| Amex Blue Biz Plus | American Express Blue Business Plus Card |
| Amex Blue Biz Cash | American Express Blue Business Cash Card |
| Venture X | Capital One Venture X Rewards Credit Card |
| Venture X Business | Capital One Venture X Business Card |
| Savor | Capital One SavorOne / Savor |
| Spark Cash Plus | Capital One Spark Cash Plus |
| Spark Miles | Capital One Spark Miles |
| Double Cash | Citi Double Cash Card |
| Custom Cash | Citi Custom Cash Card |
| Ink Preferred | Chase Ink Business Preferred |
| Ink Cash | Chase Ink Business Cash |
| Ink Unlimited | Chase Ink Business Unlimited |
| Bilt | Bilt Blue / Obsidian / Palladium |
| Robinhood | Robinhood Gold Card / Cash Card |
| Aviator Red | Barclays AAdvantage Aviator Red World Elite Mastercard |
| Wyndham Rewards | Barclays Wyndham Rewards Earner Card / Plus / Business |
| Altitude Reserve | U.S. Bank Altitude Reserve Visa Infinite Card |
| Altitude Connect | U.S. Bank Altitude Connect Visa Signature Card |
| Altitude Go | U.S. Bank Altitude Go Visa Signature Card |
| Delta Gold | American Express Delta SkyMiles Gold Card |
| Delta Platinum | American Express Delta SkyMiles Platinum Card |
| Delta Reserve | American Express Delta SkyMiles Reserve Card |
| Delta Biz Gold | American Express Delta SkyMiles Gold Business Card |
| Delta Biz Plat | American Express Delta SkyMiles Platinum Business Card |
| Delta Biz Reserve | American Express Delta SkyMiles Reserve Business Card |
