## Description: <br>
Analyzes financial news from multiple sources, classifies sentiment, assesses market, industry, and company impact, extracts key entities, and generates investment-oriented briefings for A-share, Hong Kong, and U.S. market coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SuCriss](https://clawhub.ai/user/SuCriss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and agent developers use this skill to summarize financial news, label sentiment, map news to relevant stocks or industries, and produce briefings, reports, charts, and scheduled updates. It is intended to support news triage and research workflows, not automated trading decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The main finance workflow can produce authoritative-looking reports from hardcoded articles and random sentiment labels. <br>
Mitigation: Treat generated briefings as prototype output until mock news and random sentiment paths are replaced with real fetching and validated analysis. <br>
Risk: Financial briefings and impact labels may be mistaken for trading advice. <br>
Mitigation: Use outputs only as research aids, cross-check important claims against primary sources, and do not rely on the skill alone for investment decisions. <br>
Risk: Provider-backed analysis may send news text and API credentials to selected LLM services. <br>
Mitigation: Choose an approved model provider, configure secrets through environment variables, and review what content may be shared before enabling provider-backed analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SuCriss/finance-news-analyzer) <br>
- [Supported models](references/supported-models.md) <br>
- [Configuration example](references/config-example.md) <br>
- [Industry map](references/industry-map.md) <br>
- [Sentiment rules](references/sentiment-rules.md) <br>
- [Ticker map](references/ticker-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports, JSON or CSV data exports, chart files, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include sentiment labels, confidence levels, impact assessments, stock or industry mappings, SQLite-backed history, and scheduled report generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
