## Description: <br>
Extracts structured data from webpages and APIs, with support for batch processing and JSON, CSV, or Excel-style output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and data teams use this skill to collect public webpage or API data for e-commerce monitoring, market research, job listings, real estate listings, and custom extraction workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill performs network requests against webpages and APIs, which can violate site terms or place load on services if misused. <br>
Mitigation: Use it only with sites or APIs you are authorized to access, respect robots.txt and rate limits, and configure request delays for batch jobs. <br>
Risk: Authentication values passed on the command line may be retained in shell history or process logs. <br>
Mitigation: Prefer short-lived tokens, avoid long-lived secrets on the command line, and rotate credentials after testing. <br>
Risk: Unpinned Python dependencies can reduce reproducibility for production use. <br>
Mitigation: Install in a virtual environment and pin or lock dependency versions before operational deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chungvic/ecommerce-data-scraper-pro) <br>
- [Publisher profile](https://clawhub.ai/user/chungvic) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python usage examples, and structured output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script can write JSON or CSV-like files and can fetch API responses when dependencies are installed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
