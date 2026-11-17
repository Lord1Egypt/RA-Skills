## Description:

用投资大师的脑子、呼兰的嘴，帮你搞懂指数和市场。

This skill is ready for commercial/non-commercial use.

## Publisher:

[pzc66momo](https://clawhub.ai/user/pzc66momo)

### License/Terms of Use:

MIT-0

## Use Case:

External finance readers use this skill to understand financial news, market themes, and index directions at a high level. It summarizes market logic and suggests indices to watch while avoiding personal holdings analysis, fund product recommendations, forecasts, and buy/sell advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may steer users toward Tencent Licaitong/Txfund destinations without clear upfront disclosure.

Mitigation: Review user-facing copy and index-link behavior for disclosure before deployment, especially where links or miniapp destinations are surfaced.

Risk: Financial explanations and index suggestions could be mistaken for personalized investment advice.

Mitigation: Keep the compliance disclaimer, avoid personal holdings analysis, and block fund product recommendations, return forecasts, and buy/sell/hold instructions.

Risk: The publishing script can invoke git push and the ClawHub CLI from the local environment.

Mitigation: Do not run scripts/publish-all.sh unless operating in a controlled publishing environment with trusted credentials and a pinned CLI version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pzc66momo/skills/finance-index-skill)
- [README](README.md)
- [Skill definition](SKILL.md)
- [Investment master frameworks](references/master_frameworks.md)
- [Index catalog](references/index_catalog.json)
- [Trusted index sources](references/trusted_sources_index.json)
- [Trusted media sources](references/trusted_sources_media.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Concise Chinese Markdown or plain text with market reasoning, index names and codes, optional Tencent Licaitong/Txfund links, and a compliance disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill does not provide real-time market prices, personal investment advice, fund product recommendations, return forecasts, or buy/sell/hold instructions.]

## Skill Version(s):

2.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
