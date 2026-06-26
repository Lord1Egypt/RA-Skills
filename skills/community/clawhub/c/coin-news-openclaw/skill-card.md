## Description: <br>
Collect and summarize cryptocurrency and coin market news with OpenClaw-friendly workflows. Use when users request coin news, crypto news, token-specific news, daily market briefings, or a replacement for Dify-based news aggregation. Supports configurable sources, keyword scoring, source weighting, deduplication, and structured JSON output for downstream tuning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houdl](https://clawhub.ai/user/houdl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to collect, score, deduplicate, and summarize cryptocurrency news for daily digests, token-specific monitoring, and downstream workflow handoff. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper makes public network requests to configured news feeds and CoinGecko, which can change output over time and expose normal outbound request metadata to those services. <br>
Mitigation: Review references/sources.yaml before use, run in an environment where those outbound requests are acceptable, and use --no-dynamic-tokens when deterministic or read-only token configuration is needed. <br>
Risk: Crypto-news summaries may include stale, duplicated, promotional, or misleading market information from upstream publications. <br>
Mitigation: Treat digests as news aggregation, keep source weights and negative keywords tuned in YAML, and verify important market or compliance claims against primary sources before acting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/houdl/coin-news-openclaw) <br>
- [Source registry and weights](references/sources.yaml) <br>
- [Scoring rules and token aliases](references/scoring.yaml) <br>
- [Deterministic RSS collector](scripts/fetch_coin_news.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, plus JSON or Markdown news digest output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports token, topic, time-window, limit, output-format, token-fetch-limit, and no-dynamic-token options.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
