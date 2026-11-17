## Description:

Enterprise procurement quote parsing and fraud detection for supplier quotes, cross-currency reconciliation, vendor risk auditing, and approval escalation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[d-zhangz](https://clawhub.ai/user/d-zhangz)

### License/Terms of Use:

MIT-0

## Use Case:

External business, finance, and procurement users use this skill to parse supplier quotes from messy text, OCR scans, SAP exports, HTML, CSV, or JSON, then surface calculation errors, price spikes, duplicate purchase orders, and approval recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous purchasing decisions may approve or block purchase orders without matching the organization's requester, vendor-risk, spend-limit, or approval policy.

Mitigation: Disable or wrap auto-approval behind verified requester checks, vendor-risk review, spend-limit enforcement, and human approval controls before production use.

Risk: The webhook and /license endpoints are network-facing components that can affect activation and authorization behavior if exposed broadly.

Mitigation: Install only in a controlled environment, keep these endpoints off the public internet unless protected by hardened ingress controls, and require the Lemon Squeezy webhook secret.

Risk: The PROCU_ALLOWED_TIER override can bypass normal tier checks if enabled outside local testing.

Mitigation: Do not set PROCU_ALLOWED_TIER in production and add deployment checks that fail closed when the override is present.

Risk: Optional LLM fallback can send quote-derived content to an external model provider when OPENAI_API_KEY is configured.

Mitigation: Leave OPENAI_API_KEY unset for local-only parsing, or verify the redaction behavior and data-sharing policy before enabling fallback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/d-zhangz/skills/autonomous-procurement-agent)
- [Publisher Profile](https://clawhub.ai/user/d-zhangz)

## Skill Output:

**Output Type(s):** [JSON, Guidance, Shell commands, Configuration]

**Output Format:** [Structured JSON parse results with risk alerts, recommendations, and concise setup or operating guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores, anomaly flags, fraud flags, normalized currency values, approval status, and local setup requirements.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package metadata reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
