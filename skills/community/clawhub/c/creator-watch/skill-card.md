## Description: <br>
Manage and analyze a curated watchlist of Twitter/X creators by scraping public creator content, importing it to a database, and identifying engagement patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and creator-research teams use this skill to maintain Twitter/X creator watchlists, run scraper and import commands, and analyze content performance patterns from collected public posts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill instructs users to scrape and import public Twitter/X creator content, which may implicate platform terms, rate limits, and privacy expectations. <br>
Mitigation: Confirm Twitter/X terms and privacy expectations before collection, collect only intended public content, and run scraping deliberately. <br>
Risk: The skill provides shell commands that call local scraper and importer scripts not bundled with the artifact. <br>
Mitigation: Inspect the referenced scraper and importer before execution, quote or validate usernames, and confirm output paths for JSON files and database records. <br>
Risk: Batch scraping can trigger rate limits or partial data collection. <br>
Mitigation: Use the documented delays and session limits, stop when rate limited, and report partial imports explicitly in status summaries. <br>


## Reference(s): <br>
- [Creator Watch ClawHub Listing](https://clawhub.ai/PHY041/creator-watch) <br>
- [PHY041 Publisher Profile](https://clawhub.ai/user/PHY041) <br>
- [Canlah AI Homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, SQL queries, Guidance] <br>
**Output Format:** [Markdown with inline bash and SQL code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include creator watchlists, scraping status summaries, database import steps, and engagement analysis reports.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
