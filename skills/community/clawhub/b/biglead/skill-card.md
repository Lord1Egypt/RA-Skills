## Description: <br>
BigLead helps an agent search public web sources for B2B company leads by industry, product, and region, cross-check sources, extract available contact details, and manage a local lead database. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kobenfang](https://clawhub.ai/user/kobenfang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales, market research, and competitive analysis users use this skill to identify target companies, gather publicly available business and contact information, deduplicate leads, and export prospecting records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can collect and locally store company names, business details, phone numbers, emails, and source URLs from public web sources. <br>
Mitigation: Install it only for intentional lead prospecting tasks, and review exported CSV files because they may contain contact information. <br>
Risk: Broad trigger terms such as `list` may start lead prospecting when that was not the user's intent. <br>
Mitigation: Use specific prospecting prompts and avoid vague trigger terms unless lead search is intended. <br>
Risk: Public company and contact information may be incomplete or out of date. <br>
Mitigation: Verify important lead details against current official or primary sources before outreach. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kobenfang/biglead) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown lead reports with inline shell commands, plus local JSON and CSV lead data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores lead records, search history, and CSV exports under memory/lead-data/.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
