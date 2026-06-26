## Description: <br>
Navigate FRED categories and series using fredapi, supporting natural-language queries with intent recognition and double validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kiszly](https://clawhub.ai/user/kiszly) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and agent users use this skill to navigate Federal Reserve Economic Data categories, discover series, and retrieve series data or metadata from FRED using category IDs, series IDs, or natural-language queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script disables HTTPS certificate verification while using a FRED API key. <br>
Mitigation: Remove the SSL context override before use and verify FRED API calls with normal certificate validation enabled. <br>
Risk: The skill requires network access to FRED and a FRED_API_KEY environment variable. <br>
Mitigation: Install and run it in an isolated environment, provide the API key only through the environment, and avoid committing credentials to skill files. <br>
Risk: Unpinned Python dependencies can reduce reproducibility and assurance. <br>
Mitigation: Pin dependency versions before deployment when reproducible or higher-assurance operation is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kiszly/fred-navigator) <br>
- [README.md](README.md) <br>
- [fred_categories_tree.json](references/fred_categories_tree.json) <br>
- [fred_categories_flat.json](references/fred_categories_flat.json) <br>
- [category_paths.json](references/category_paths.json) <br>
- [synonyms.json](references/synonyms.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON or table outputs from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include FRED category candidates, series metadata, recent series values, missing-count summaries, and latest value/date details.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
