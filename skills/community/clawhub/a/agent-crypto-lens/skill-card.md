## Description:

Analyzes cryptocurrency token market trends and sentiment using market data, web news, and LLM-generated summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinu4you](https://clawhub.ai/user/jinu4you)

### License/Terms of Use:

ISC

## Use Case:

External users and developers use this skill to request cryptocurrency token market, news sentiment, and score summaries for informational analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Token queries, market/news context, and generated prompts may be sent to third-party APIs.

Mitigation: Use restricted API keys and avoid submitting secrets, private portfolio details, or non-public investment information.

Risk: Generated market and sentiment reports may contain inaccurate, stale, or incomplete analysis.

Mitigation: Treat outputs as informational and verify market data, news sources, and score rationale before making financial or operational decisions.

Risk: Output-integrity and disclosure gaps may make production use harder to audit.

Mitigation: Add stronger input validation, dependency review, and clear disclosure of external API use before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jinu4you/skills/agent-crypto-lens)
- [ClawHub Publisher Profile](https://clawhub.ai/user/jinu4you)
- [Tavily Search API Endpoint](https://api.tavily.com/search)
- [CoinGecko API Search Endpoint](https://api.coingecko.com/api/v3/search)
- [CoinGecko API Coin Detail Endpoint](https://api.coingecko.com/api/v3/coins/{coinId})
- [Google Generative Language API Endpoint](https://generativelanguage.googleapis.com/v1/models/{model}:generateContent)
- [Groq OpenAI-Compatible API Endpoint](https://api.groq.com/openai/v1)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [JSON object containing market data, sentiment labels, markdown report text, and numeric scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts a token and optional analysis_type; reports should be treated as informational rather than financial advice.]

## Skill Version(s):

1.0.1 (source: server release metadata and package.json; SKILL.md frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
