## Description: <br>
Google Analytics 4, Search Console, and Indexing API toolkit for analyzing website traffic, page performance, user demographics, real-time visitors, search queries, SEO metrics, URL indexing status, and e-commerce revenue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adamkristopher](https://clawhub.ai/user/adamkristopher) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, site owners, and SEO or analytics operators use this skill to pull GA4, Search Console, and Google Indexing API data, compare date ranges, inspect URLs, and create saved summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes a Google URL removal action that can request URL deletion from Google's index. <br>
Mitigation: Do not expose or invoke removeFromIndex() unless URL removal is explicitly required, and require confirmation for each URL before use. <br>
Risk: Google service account credentials and analytics exports may expose sensitive site or business data. <br>
Mitigation: Use a dedicated least-privilege Google service account limited to the intended GA4 property and Search Console site, and keep .env and results/ out of version control. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [ClawHub GA4 Analytics skill page](https://clawhub.ai/adamkristopher/ga4-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls, Files] <br>
**Output Format:** [Markdown guidance with TypeScript examples, shell commands, Google API responses, saved JSON files, and markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results are saved under results/ by category when the skill functions run with saving enabled.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and scripts/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
