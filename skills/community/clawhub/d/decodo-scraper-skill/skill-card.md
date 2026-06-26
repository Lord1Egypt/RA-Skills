## Description: <br>
Search Google, scrape web pages, Amazon product pages, YouTube subtitles, or Reddit (post/subreddit) using the Decodo Scraper OpenClaw Skill. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DonatasDecodo](https://clawhub.ai/user/DonatasDecodo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to retrieve web search results, public webpage content, marketplace data, video transcripts, and Reddit content through Decodo's scraping API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted URLs, search terms, video IDs, and scraping requests are sent to Decodo. <br>
Mitigation: Use a dedicated Decodo token and avoid submitting sensitive internal URLs, regulated data, or confidential queries. <br>
Risk: The skill requires a Decodo authentication token. <br>
Mitigation: Keep DECODO_AUTH_TOKEN out of shared repositories and rotate it if it may have been exposed. <br>
Risk: Unpinned dependencies can change behavior in controlled or production environments. <br>
Mitigation: Pin and review dependencies before production deployment. <br>


## Reference(s): <br>
- [Decodo](https://decodo.com) <br>
- [Decodo Web Scraping API Google Search documentation](https://help.decodo.com/docs/web-scraping-api-google-search) <br>
- [Decodo Web Scraping API](https://decodo.com/scraping/web) <br>
- [ClawHub skill page](https://clawhub.ai/DonatasDecodo/decodo-scraper-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [JSON, Markdown, plain text transcripts, and command-line setup instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires DECODO_AUTH_TOKEN and sends submitted URLs, queries, and video IDs to Decodo.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
