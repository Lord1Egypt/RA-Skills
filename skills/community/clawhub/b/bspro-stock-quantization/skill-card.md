## Description:

BSpro Stock Quantization helps agents query and analyze China A-share market data, run technical indicators and backtests, and produce MOE-factor stock signal reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eventaumjohn](https://clawhub.ai/user/eventaumjohn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer A-share stock research questions, retrieve price and sector data, generate buy/sell signal reports, and run factor-mining or backtest workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token-bearing remote update requests may expose credentials when sent over HTTP.

Mitigation: Install only if the BitSoul service is trusted, use a scoped token, and require token-bearing endpoints to use HTTPS before production deployment.

Risk: Remote data patches are imported in unsafe ways and could execute code or corrupt local data if compromised.

Mitigation: Accept patches only from signed or digest-verified manifests, remove pickle-based patch loading, and extract archives with path validation.

Risk: Verbose logs or embedded sample credentials can disclose sensitive access material.

Mitigation: Remove hard-coded tokens and redact detailed logs by default before use.

Risk: Retraining and cache-clearing workflows can change local analysis state in ways users may not expect.

Mitigation: Make retraining and cache-clearing actions explicit, reversible, and documented for operators.

## Reference(s):

- [StockApi interface documentation](references/API_FOR_LLM.md)
- [BSpro Stock Quantization on ClawHub](https://clawhub.ai/eventaumjohn/skills/bspro-stock-quantization)
- [BitSoul homepage](https://www.aicodingyard.com)
- [Sina Finance](https://finance.sina.com.cn/)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Simplified Chinese Markdown reports with structured JSON data when returned by the skill APIs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BITSOUL_TOKEN for data access; optional BITSOUL_TOKEN_ENV_FILE and BITSOUL_CACHE_DIR control token loading and cache location.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
