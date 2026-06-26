## Description: <br>
Fetch and parse news highlights from CCTV News Broadcast (Xinwen Lianbo) for a given date. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve CCTV News Broadcast summaries for a specific date and have an agent present the resulting highlights in a readable summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The crawler can follow links discovered in remote CCTV/CNTV pages. <br>
Mitigation: Review before installation and restrict follow-up requests to explicit CCTV hosts over HTTPS, with rejected links logged or skipped. <br>
Risk: The crawler sends a bundled cookie header during normal web requests. <br>
Mitigation: Remove the static cookie unless it is explicitly required and approved for the deployment. <br>
Risk: Unbounded or slow web requests can make the skill unreliable or increase operational exposure. <br>
Mitigation: Add request limits and timeouts before using the skill in a production workflow. <br>
Risk: Running commands outside the authorized crawler script increases command-execution scope. <br>
Mitigation: Limit execution to bun or node running scripts/news_crawler.js with a single YYYYMMDD argument; do not run package managers, shell pipelines, or output redirection as part of normal use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/cctv-news-fetcher-hardened) <br>
- [Publisher profile](https://clawhub.ai/user/snazar-faberlens) <br>
- [Faberlens safety evaluation](https://faberlens.ai/explore/cctv-news-fetcher) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown summary based on JSON returned by a local news crawler script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The crawler is invoked for one YYYYMMDD date value and returns a list of news items with date, title, and content fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
