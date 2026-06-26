## Description: <br>
Autonomous financial research agent for stock analysis, financial statements, metrics, prices, SEC filings, and crypto data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use Dexter to ask financial research questions and receive synthesized analysis across stocks, crypto, company fundamentals, SEC filings, metrics, prices, news, and comparisons. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installation pulls and runs unpinned third-party code. <br>
Mitigation: Review or pin the Dexter repository commit before installation, then run it as a non-root user in an isolated workspace. <br>
Risk: The skill requires API keys and sends research queries to external providers. <br>
Mitigation: Use dedicated low-privilege API keys and avoid submitting confidential financial plans, watchlists, client data, or proprietary research unless the provider data handling is acceptable. <br>
Risk: Financial answers can depend on external data coverage and model synthesis. <br>
Mitigation: Verify important outputs against primary sources before relying on them for financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-dexter) <br>
- [SkillBoss API Hub](https://api.heybossai.com) <br>
- [Financial Datasets](https://financialdatasets.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use external API-backed financial research queries when the required API keys are configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
