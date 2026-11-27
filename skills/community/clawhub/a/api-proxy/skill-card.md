## Description:

API Gateway is a local Node.js proxy for outbound API calls with retries, metadata-only caching by default, rate-limit handling, circuit breaking, fallback providers, and API key management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlacroix82](https://clawhub.ai/user/jlacroix82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to centralize outbound HTTP API calls through a reusable gateway with retry, fallback, rate-limit, cache, request-log, and API-key handling controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gateway handles provider credentials and can store API keys as plaintext in the local workspace.

Mitigation: Prefer PROVIDER_API_KEY environment variables or a secrets manager, use tightly scoped allowlisted stored keys only when needed, and remove local keys after sensitive work.

Risk: Requests, prompts, headers, bodies, and responses are transmitted to the third-party provider endpoint selected by the caller.

Mitigation: Send requests only to trusted endpoints, review provider retention policies, and avoid routing sensitive or regulated data through untrusted providers.

Risk: Full-body caching can persist complete responses that may contain secrets, personal data, or proprietary content.

Mitigation: Keep the default metadata-only cache, avoid --cache-full for sensitive providers, and clear cache and log files after sensitive sessions.

Risk: Plain HTTP can expose traffic when API_GATEWAY_ALLOW_HTTP=1 is enabled.

Mitigation: Use HTTPS endpoints and never enable API_GATEWAY_ALLOW_HTTP=1 when credentials or sensitive payloads may be attached.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlacroix82/skills/api-proxy)
- [README](README.md)
- [Vetting report](VET-REPORT.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [CLI text, JSON API responses, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform outbound HTTP API calls and write local gateway state, including keys, cache metadata, request logs, rate-limit state, circuit state, and fallback mappings.]

## Skill Version(s):

1.1.12 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
