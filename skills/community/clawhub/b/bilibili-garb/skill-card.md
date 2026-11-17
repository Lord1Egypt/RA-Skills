## Description:

Bilibili Garb supports Bilibili personalization item collection and management, including garb search, suit or collection detail lookup, owned benefit scans, discontinued item recovery, and scarcity-tier checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuangzhanzhiwang](https://clawhub.ai/user/kuangzhanzhiwang)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and operators use this skill to search Bilibili personalization items, inspect garb suit or collection details, recover discontinued item data, and scan owned benefit sub-items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses Bilibili account session credentials, including access keys and cookies, which can expose the account if stored or logged carelessly.

Mitigation: Store credentials outside shared workspaces with restrictive permissions, never commit configs/bili-api-creds.json, rotate credentials after use, and install only when account-session access is acceptable.

Risk: Packet capture and browser cookie collection can reveal live account secrets beyond what is needed for a single lookup.

Mitigation: Avoid casual packet capture or cookie extraction, collect only the minimum required credentials, and remove captured data after credential setup is complete.

Risk: Debug and curl examples may expose credentials in terminal history, logs, or retained output.

Mitigation: Avoid debug mode and credential-bearing curl commands in logged environments; redact tokens from command history and shared transcripts.

## Reference(s):

- [Bilibili Garb API Reference](references/bilibili-garb-api-reference.md)
- [Bilibili Garb SOP](references/bilibili-garb-sop.md)
- [ClawHub Skill Page](https://clawhub.ai/kuangzhanzhiwang/skills/bilibili-garb)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, shell command guidance, JSON configuration examples, and NDJSON scan results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and detail commands query Bilibili APIs and optional local gallery data; the benefit scanner can append records to data/garb-benefit-results.ndjson.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
