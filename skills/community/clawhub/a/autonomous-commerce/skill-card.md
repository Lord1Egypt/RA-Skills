## Description:

Autonomous Commerce helps agents execute constrained physical e-commerce purchases with escrow protection and proof-hash confirmation when budget, saved payment, and saved shipping prerequisites are satisfied.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pandeyaby](https://clawhub.ai/user/pandeyaby)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to let an agent complete tightly scoped retail purchases, return order confirmation with proof, and settle escrow after verification. It is for purchase execution after intent and budget are clear, not general product research or price comparison.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can drive a real checkout session and spend money using saved payment and shipping details.

Mitigation: Use a tightly controlled account, require explicit per-purchase confirmation, and verify the final total against the approved budget before order placement.

Risk: Order evidence and screenshots may contain payment, address, or purchase details.

Mitigation: Store evidence securely, redact personal information before sharing, and delete evidence after verification when retention is not required.

Risk: Escrow release and proof validation may be insufficient for high-value or production purchases.

Mitigation: Require real escrow state checks, authoritative proof validation, and manual review until the release has stronger payment-safety controls.

Risk: Browser automation may fail or behave unpredictably on CAPTCHA, out-of-stock, duplicate-order, or payment-decline flows.

Mitigation: Pause for human intervention on exceptional checkout states and refund or keep escrow locked until the purchase outcome is verified.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pandeyaby/skills/autonomous-commerce)
- [Moltbook proof-of-concept post](https://moltbook.com/post/8cc8ee6b-8ce5-40d8-81e9-abf5a33d7619)
- [Moltbook ClawPay integration post](https://moltbook.com/post/86ffca5e-c57b-497d-883d-688c29d6cf88)
- [OpenAI skills shell tips](https://developers.openai.com/blog/skills-shell-tips)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with order-confirmation templates, JavaScript examples, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns purchase confirmations, proof hashes, escrow status, and setup guidance; requires agent access to browser automation and preconfigured accounts.]

## Skill Version(s):

1.0.0 (source: release metadata, package.json, skill.json, CHANGELOG released 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
