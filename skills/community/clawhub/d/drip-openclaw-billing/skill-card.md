## Description:

Add usage metering and billing telemetry to OpenClaw agents using Drip for per-run cost attribution, tool-call usage tracking, and customer-level billing visibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucas-309](https://clawhub.ai/user/lucas-309)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to instrument OpenClaw agents with Drip billing telemetry, including run lifecycle events, tool-call usage metering, and customer-level cost attribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Billing telemetry could expose sensitive prompts, outputs, credentials, PII, or raw request bodies if callers send unsanitized data.

Mitigation: Send sanitized metadata only, keep the documented restriction against raw prompts, raw outputs, credentials, PII, and raw request bodies, and hash content fields such as query fingerprints when needed.

Risk: Incorrect telemetry endpoint or credential scope could route billing data to the wrong Drip environment or over-privileged key.

Mitigation: Use scoped telemetry keys, verify DRIP_BASE_URL before production, and prefer the documented DRIP_API_KEY path for complete run, event, and usage telemetry.

Risk: Retries can duplicate billable usage events if writes are not idempotent.

Mitigation: Emit stable idempotency keys for writes and verify in staging that retries do not create duplicate usage records.

## Reference(s):

- [Drip OpenClaw Billing API Reference](artifact/references/API.md)
- [ClawHub skill page](https://clawhub.ai/lucas-309/skills/drip-openclaw-billing)
- [ClawHub publisher profile](https://clawhub.ai/user/lucas-309)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with TypeScript, Python, and shell snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes sanitized telemetry metadata, scoped credentials, idempotency keys, and fail-open billing writes.]

## Skill Version(s):

1.1.1 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
