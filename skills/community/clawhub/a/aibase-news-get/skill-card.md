## Description: <br>
Fetches recent AIBase news pages, extracts article details, and stores structured local news data for AI news collection, aggregation, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiahuishao](https://clawhub.ai/user/jiahuishao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators can use this skill to collect recent AIBase articles into a local JSON news feed for aggregation, summary workflows, and public-opinion monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches live AIBase web pages and stores scraped article data locally. <br>
Mitigation: Install and run it only where fetching AIBase pages and retaining scraped article content is acceptable. <br>
Risk: The default behavior creates a News directory and updates news_latest.json in the current working directory. <br>
Mitigation: Run it from a controlled directory, or pass an explicit output directory through the Python API when tighter file placement is required. <br>


## Reference(s): <br>
- [AIBase news source](https://www.aibase.com/zh/news) <br>
- [ClawHub skill page](https://clawhub.ai/jiahuishao/aibase-news-get) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, Markdown] <br>
**Output Format:** [Console text plus local JSON news data and optional Markdown article files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes crawl results to a local News directory and updates news_latest.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
