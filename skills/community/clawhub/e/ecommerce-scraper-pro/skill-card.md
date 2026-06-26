## Description: <br>
Extracts structured data from web pages and APIs, with support for batch processing and multiple output formats. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to collect structured product, article, job, real estate, social, or custom data from permitted web and API sources. It is suited for workflows such as price monitoring, market research, and lead data collection where the user controls scraping scope and outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The scraper performs user-directed network requests and may access sites where scraping is restricted. <br>
Mitigation: Only scrape sites and APIs you are allowed to access, respect robots.txt and rate limits, and avoid excessive request volume. <br>
Risk: API authentication values passed with --auth could expose sensitive credentials if reused broadly or logged outside the tool. <br>
Mitigation: Use scoped temporary API tokens, avoid collecting sensitive personal data, and rotate credentials after use when appropriate. <br>
Risk: The tool writes results to user-supplied output paths and creates parent directories. <br>
Mitigation: Choose output paths intentionally, review generated files before sharing them, and run the skill in a virtual environment with pinned or locked dependencies when reproducibility matters. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands; the scraper can produce JSON, CSV, or Excel-style output files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on user-selected URLs, API endpoints, selectors, data type, authentication, delay, and output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
