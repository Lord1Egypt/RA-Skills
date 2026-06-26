## Description: <br>
One-click automated pipeline for AI product launch monitoring, including RSS monitoring, product search enrichment, screenshot capture, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and market intelligence teams use this skill to monitor AI product launch feeds, enrich launch records, capture optional page screenshots, and generate trend reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring runs can make repeated network requests to configured RSS feeds and search endpoints. <br>
Mitigation: Review the RSS feed configuration before running and enable the cron example only when recurring network access is intended. <br>
Risk: Optional screenshot capture opens product pages and saves local PNG files. <br>
Mitigation: Use --skip-screenshot in sensitive or restricted environments. <br>
Risk: The pipeline saves local launch data, enrichment results, screenshots, and analysis reports. <br>
Mitigation: Use the PIPELINE_DATA_DIR, PIPELINE_SCREENSHOT_DIR, and PIPELINE_ANALYSIS_DIR settings to control output locations and review files before sharing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/ai-launch-pipeline) <br>
- [Publisher profile](https://clawhub.ai/user/terrycarter1985) <br>
- [Skill instructions](SKILL.md) <br>
- [RSS feed configuration](config/rss_feeds.yaml) <br>
- [DuckDuckGo HTML Search](https://html.duckduckgo.com/html/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON files, PNG screenshots, Markdown report, and terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local data, screenshots, and analysis directories; screenshots are optional.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
