## Description: <br>
Fetches recent CNBC geopolitical news articles, extracts factual market and event details, and posts article briefings to Discord or a Markdown output file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dimaschand29](https://clawhub.ai/user/dimaschand29) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to collect recent CNBC geopolitics articles, extract market-impact and hard-fact snippets, avoid reposting previously sent URLs, and deliver the briefings to Discord or Markdown for monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes a real-looking Discord webhook and directs agents to use it. <br>
Mitigation: Revoke and remove the bundled webhook, provide a user-controlled secret outside the skill files, and confirm the Discord channel before each run. <br>
Risk: Running the skill sends CNBC-derived article content and extracted facts to Discord. <br>
Mitigation: Use an isolated Python environment and treat each execution as publishing content to the selected Discord channel. <br>
Risk: Scraping and keyword extraction can miss, duplicate, or misclassify article facts and market impact. <br>
Mitigation: Review generated briefings before relying on them for trading, operational, or decision-support workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dimaschand29/cnbc-geopolitics-fetcher) <br>
- [CNBC World](https://www.cnbc.com/world/) <br>
- [CNBC Finance](https://www.cnbc.com/finance/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands] <br>
**Output Format:** [Discord message text and Markdown briefing with article titles, URLs, market impact, and hard facts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Posts each article separately, splits long Discord messages near the 2000-character platform limit, and can write an output file.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
