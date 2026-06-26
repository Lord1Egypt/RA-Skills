## Description: <br>
Collects daily news from configured RSS feeds and webpages, then helps an agent filter, classify, summarize, and produce structured Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[winsaney](https://clawhub.ai/user/winsaney) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operators, and developers use this skill to gather configured public news sources, monitor topics such as industry activity or competitors, and generate concise daily Markdown reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured feeds or URL lists could point at private, internal, or sensitive pages. <br>
Mitigation: Review RSS feed configuration, URL lists, and output paths before use; avoid private or sensitive targets. <br>
Risk: Web collection may conflict with a target site's terms, robots.txt, or rate limits. <br>
Mitigation: Use respectful collection rates and confirm target site permissions before scraping. <br>
Risk: Daily reports may summarize unverified, outdated, or misleading source material. <br>
Mitigation: Review important items and source links before relying on the generated report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/winsaney/daily-news-collector) <br>
- [Media Source Configuration Guide](artifact/references/sources.md) <br>
- [Daily Report Format Guide](artifact/references/format.md) <br>
- [Daily Report Template](artifact/assets/template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily reports with source links and summary sections; collection scripts write JSON data files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on configured RSS feeds, webpage URLs, topic filters, and the agent's summarization choices.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
