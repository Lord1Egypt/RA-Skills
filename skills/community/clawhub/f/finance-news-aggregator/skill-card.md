## Description: <br>
Aggregates AI, technology, and finance news into source-aware summaries, ranking frameworks, translations, and risk-monitoring guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gechengling](https://clawhub.ai/user/gechengling) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill as a reference workflow for collecting AI, technology, and finance news, summarizing important items, translating selected English-language stories, and flagging items that need source verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-impact summaries, sentiment labels, and risk ratings may be incomplete, stale, or misleading if sources are not checked. <br>
Mitigation: Verify original sources before acting and treat all market-impact and risk sections as informational rather than financial, legal, or insurance advice. <br>
Risk: Separate user-deployed Python scripts may contact RSS feeds or third-party APIs and expose query terms, IP address, timestamps, or similar request metadata. <br>
Mitigation: Review any separate script before deployment, confirm third-party terms and robots.txt expectations, and limit data sent to external feeds or APIs. <br>
Risk: The release is documentation-only and describes aggregation frameworks and code examples without included executable code. <br>
Mitigation: Treat commands and configuration as examples that require local review, testing, and security scanning before operational use. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/gechengling/finance-news-aggregator) <br>
- [OpenAI Blog RSS feed](https://openai.com/blog/rss.xml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with example shell commands, configuration snippets, scoring tables, and summary templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; any separate scripts or external feed access are user-deployed and should be reviewed before use.] <br>

## Skill Version(s): <br>
5.0.3 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
