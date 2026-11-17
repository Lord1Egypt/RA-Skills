## Description:

DeepKnow Currency helps agents query and convert CNY exchange rates for USD, EUR, JPY, and GBP, and route paid alert or forecast requests through JD clawtip against the configured InkRate endpoint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oicqren](https://clawhub.ai/user/oicqren)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check recent CNY exchange rates, calculate CNY-linked conversions, and request paid exchange-rate alerts or forecast-style probability results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security verdict is suspicious because payment credential handling is under-scoped enough to require careful review before installation.

Mitigation: Install only if the publisher and configured InkRate endpoint are trusted, and review the payment flow before using paid services.

Risk: A custom base URL can redirect exchange-rate and payment fulfillment requests to a replacement service.

Mitigation: Keep the default HTTPS host unless the replacement service is controlled and trusted.

Risk: Local order files can contain payment credentials and personal request details.

Mitigation: Treat order files as sensitive and avoid shared or world-writable order directories.

## Reference(s):

- [DeepKnow Currency ClawHub page](https://clawhub.ai/oicqren/skills/deepknow-currency)
- [Publisher profile](https://clawhub.ai/user/oicqren)
- [InkRate default service endpoint](https://rate.feedai.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Plain text status lines, key-value exchange-rate fields, JSON fulfillment results, and Markdown guidance from the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid services use order numbers and payment status values; free conversion is limited to paths involving CNY.]

## Skill Version(s):

0.1.8 (source: server release metadata and manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
