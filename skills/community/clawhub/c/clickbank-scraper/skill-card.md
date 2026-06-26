## Description: <br>
Scrape top ClickBank products by category with gravity scores, commission rates, and estimated monthly sales for affiliate marketing automation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marlowne12](https://clawhub.ai/user/marlowne12) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and affiliate marketing operators use this skill to run a Node.js scraper that collects ClickBank Health & Fitness product metrics from CBTrends and prepares JSON outputs for downstream automation such as Pinterest content, comparison pages, and performance tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper contacts CBTrends and writes local output files during execution. <br>
Mitigation: Run it only in an environment where that network access and local file writes are expected, and review scheduled cron or n8n use before enabling it. <br>
Risk: A configured CB_AFFILIATE_ID appears in generated hoplinks and may appear in console output or saved JSON. <br>
Mitigation: Use only the intended affiliate nickname and avoid sharing generated output where that identifier should remain private. <br>
Risk: The product metrics are scraped public marketplace data and the artifact notes that gravity data may lag live marketplace values. <br>
Mitigation: Treat generated product rankings as automation inputs and verify important business decisions against current marketplace data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marlowne12/clickbank-scraper) <br>
- [CBTrends Health & Fitness Marketplace Source](https://www.cbtrends.com/browse-clickbank-marketplace/-1/94/Health%2B%2526%2BFitness/1/gravity/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON files, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; scraper execution writes JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/latest.json, output/products-YYYY-MM-DD.json, and output/top10-YYYY-MM-DD.json; optional CB_AFFILIATE_ID is embedded in generated hoplinks.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
