## Description:

Collect and summarize cryptocurrency and coin market news with OpenClaw-friendly workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[houdl](https://clawhub.ai/user/houdl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to collect, filter, score, deduplicate, and summarize cryptocurrency news for daily briefings, token-specific updates, or downstream workflow handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts multiple crypto news RSS sources and CoinGecko during normal collection.

Mitigation: Run it only in environments where outbound network access to those sources is acceptable, and disable dynamic token fetching with --no-dynamic-tokens when the CoinGecko call or cache update is not desired.

Risk: Fetched article content and links are third-party data and may be misleading, stale, or unsafe to follow.

Mitigation: Treat article summaries and links as untrusted inputs, review sources before relying on results, and avoid adding RSS feeds that are not trusted.

Risk: Dynamic token fetching can update references/scoring.yaml with a local token cache.

Mitigation: Review cache changes before committing or distributing the skill, or use --no-dynamic-tokens for read-only scoring behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/houdl/skills/coin-news-openclaw)
- [Source registry and weights](references/sources.yaml)
- [Scoring configuration](references/scoring.yaml)
- [Deterministic RSS collector and scorer](scripts/fetch_coin_news.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, plus JSON or Markdown digest output from the bundled script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can filter by lookback window, token, topic, result limit, output format, and dynamic token fetching mode.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
