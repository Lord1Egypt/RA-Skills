## Description: <br>
Cross-references restaurant recommendations from Xiaohongshu and Dianping by location and cuisine, comparing ratings, review counts, engagement, sentiment, and cross-platform consistency to produce confidence-scored recommendations. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[zhongrenfei1-hub](https://clawhub.ai/user/zhongrenfei1-hub) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and researchers use this skill to compare restaurant signals across Dianping and Xiaohongshu for location- and cuisine-specific recommendation research. It is most appropriate when outputs will be reviewed against platform terms and source data before use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reuse saved logged-in browser sessions for scraping Dianping and Xiaohongshu. <br>
Mitigation: Use isolated accounts where possible, inspect and clean saved sessions before and after runs, and avoid sharing session artifacts. <br>
Risk: Default output may appear validated even when generated from mock or simulated data. <br>
Mitigation: Treat recommendations as simulated unless the real scraper is explicitly run, and verify source data before relying on results. <br>
Risk: Scraping and proxy-based access may conflict with platform terms or trigger account and IP controls. <br>
Mitigation: Review platform terms before use, apply conservative rate limits, and avoid storing personal user data. <br>


## Reference(s): <br>
- [Data schema documentation](artifact/references/data_schema.md) <br>
- [Sentiment analysis guide](artifact/references/sentiment_analysis.md) <br>
- [API and data source limitations](artifact/references/api_limitations.md) <br>
- [SnowNLP documentation](https://github.com/isnowfy/snownlp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style restaurant recommendation report with ranked results, scores, platform comparisons, and warnings.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces up to 5-10 ranked restaurant recommendations with consistency levels, confidence scores, and discrepancy notes.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
