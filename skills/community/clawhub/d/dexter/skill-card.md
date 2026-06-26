## Description: <br>
Autonomous financial research agent for stock analysis, financial statements, metrics, prices, SEC filings, and crypto data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[igorhvr](https://clawhub.ai/user/igorhvr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use Dexter to ask financial research questions about stocks, crypto, company fundamentals, market data, SEC filings, analyst estimates, insider trades, and company news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs a separate upstream project with Bun and local dependencies. <br>
Mitigation: Review the project before execution and install only in an environment appropriate for running third-party code. <br>
Risk: The skill stores LLM, financial-data, and web-search API keys in a local .env file. <br>
Mitigation: Use least-privilege API keys, keep .env out of git, restrict file permissions such as with chmod 600, and rotate keys if exposed. <br>
Risk: Financial research questions may be sent to third-party LLM, financial-data, and web-search providers. <br>
Mitigation: Avoid entering confidential watchlists, internal investment research, or other sensitive financial data unless those providers are approved for that data. <br>
Risk: Financial Datasets API coverage is primarily for US stocks, with international coverage relying on web search fallback. <br>
Mitigation: Check source coverage and verify answers for international securities before relying on them. <br>


## Reference(s): <br>
- [ClawHub Dexter listing](https://clawhub.ai/igorhvr/dexter) <br>
- [Financial Datasets API](https://financialdatasets.ai) <br>
- [Tavily](https://tavily.com) <br>
- [Anthropic Console](https://console.anthropic.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented guidance with shell commands and generated financial research answers.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use local environment variables for Anthropic, Financial Datasets, Tavily, and OpenAI API keys; complex queries may take 30-60 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
