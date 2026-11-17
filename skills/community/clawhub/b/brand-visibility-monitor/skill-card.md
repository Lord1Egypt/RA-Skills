## Description:

Brand Visibility Monitor checks brand keyword visibility across AI search platforms, generates a 0-100 GEM score, analyzes why a brand may not be recommended, and can push reports to Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yk-global-01](https://clawhub.ai/user/yk-global-01)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, and growth teams use this skill to monitor whether target brands and competitors appear in AI platform responses and to receive concise visibility scores, reports, and optimization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Brand names, search prompts and results, license checks, and optional reports may be sent to external AI platforms, yk-global, Tavily, and Feishu.

Mitigation: Install only when this data sharing is acceptable, review configured endpoints and webhooks before use, and avoid submitting confidential brand information unless approved.

Risk: The bundled API service uses placeholder API key handling and lacks production-grade authentication and rate limits.

Mitigation: Do not deploy the API service as-is; replace placeholder keys, add real authentication, enforce rate limits, and perform a deployment security review.

Risk: Local upgrade state and temporary report handling can affect usage controls or leave generated reports on disk.

Mitigation: Validate entitlement logic before commercial deployment and manage generated report files according to local retention and access-control requirements.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yk-global-01/skills/brand-visibility-monitor)
- [YK Global](https://yk-global.com)
- [YK Global API Key Verification Endpoint](https://api.yk-global.com/v1/verify)
- [Tavily](https://tavily.com)
- [Tavily Search API Endpoint](https://api.tavily.com/search)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, console status text, configuration guidance, and optional Feishu notification payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include platform-level visibility results, a GEM score, excerpts, and optimization guidance.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
