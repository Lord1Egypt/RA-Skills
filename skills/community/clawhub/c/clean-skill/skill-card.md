## Description:

Cross-reference restaurant recommendations from Xiaohongshu and Dianping to validate restaurant quality and consistency by location and cuisine, producing confidence-scored recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhongrenfei1-hub](https://clawhub.ai/user/zhongrenfei1-hub)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to compare restaurant signals from Dianping and Xiaohongshu for a requested location and cuisine. It helps identify higher-confidence restaurant recommendations and flags low-consistency matches for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store logged-in browser session data locally.

Mitigation: Run it in an isolated environment, keep the sessions directory private, and never share or commit saved session data.

Risk: The skill relies on scraping Dianping and Xiaohongshu for real data paths.

Mitigation: Review applicable platform terms before use and prefer approved data access methods for production or commercial workflows.

Risk: Default fetchers may return mock data while appearing to perform live collection.

Mitigation: Treat default results as synthetic unless the real scraper path is explicitly used and validated.

## Reference(s):

- [Data schema documentation](references/data_schema.md)
- [Sentiment analysis guide](references/sentiment_analysis.md)
- [API and data source limitations](references/api_limitations.md)
- [Dianping](https://www.dianping.com)
- [Xiaohongshu](https://www.xiaohongshu.com)
- [SnowNLP documentation](https://github.com/isnowfy/snownlp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style restaurant recommendation text with ranked results, scores, platform comparisons, warnings, and optional shell commands or configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendation scores use a 0-10 scale; consistency levels are high, medium, or low.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
