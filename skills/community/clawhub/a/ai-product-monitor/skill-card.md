## Description: <br>
One-click AI product launch monitoring pipeline: RSS monitoring, product info search, screenshot capture, and trend analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and product teams use this skill to monitor configured AI product launch feeds, enrich discovered launches, capture launch-page screenshots, and generate a trend report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured feeds and collected launch URLs can direct the pipeline to untrusted external sites. <br>
Mitigation: Review references/feeds.yaml before running and inspect collected URLs with individual stages before screenshot capture. <br>
Risk: The screenshot stage may access URLs from monitored feeds from the execution environment. <br>
Mitigation: Avoid running the screenshot stage in environments that can reach private internal services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/ai-product-monitor) <br>
- [RSS feed configuration](references/feeds.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [JSON launch data, PNG screenshots, and a Markdown trend report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local artifacts under data/: raw_launches.json, enriched_launches.json, screenshots, and trend_report.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
