## Description: <br>
Google Search Console sitemap status skill for MyBrandMetrics that queries connected sitemap data, submitted URL counts, indexed URL counts, warnings, errors, pending processing status, content type, and last downloaded time through the google_search_console_sitemaps source. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawbus](https://clawhub.ai/user/clawbus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and SEO operators use this skill to query MyBrandMetrics for Google Search Console sitemap health, including submitted and indexed URLs, warnings, errors, pending rows, content type, and last downloaded time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive MyBrandMetrics credentials and a connected Google Search Console property. <br>
Mitigation: Prefer the MYBRANDMETRICS_API_KEY environment variable, avoid logging secrets, and redact credentials before sharing output. <br>
Risk: Queries can return incomplete or stale sitemap status because Google Search Console data may lag by several days. <br>
Mitigation: Treat recent sitemap submissions or indexing changes as delayed and verify connection IDs, filters, and property setup when rows are missing. <br>
Risk: The security review advises deliberate approval of powerful commands. <br>
Mitigation: Review shell commands before running them and install the skill only in workspaces where the expected connected services are authorized. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/clawbus/clawbus-google-search-console) <br>
- [Publisher profile](https://clawhub.ai/user/clawbus) <br>
- [Configuration](references/configuration.md) <br>
- [Dimensions and Metrics](references/dimensions.md) <br>
- [Query Patterns](references/query-patterns.md) <br>
- [MyBrandMetrics](https://mybrandmetrics.com/) <br>
- [Clawbus](https://www.clawbus.com/) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a MyBrandMetrics API key and Google Search Console connection ID; supports filters, metric selection, dimension selection, limits, and compact JSON output.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
