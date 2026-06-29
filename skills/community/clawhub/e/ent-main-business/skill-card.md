## Description: <br>
Generates a structured main-business and core-product analysis report from a company name by querying enterprise-search and business-analysis APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daviddatamining](https://clawhub.ai/user/daviddatamining) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, business-development teams,招商 teams, and due-diligence analysts use this skill to identify a target company, retrieve enterprise business data, and produce a concise report explaining what the company does and which products or services matter. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends company names or enterprise IDs to a disclosed external enterprise-information API, and the helper script can print full request and response details to the terminal. <br>
Mitigation: Use it only with data appropriate for that external API, avoid confidential research unless terminal output is acceptable, and review generated reports before sharing or relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daviddatamining/ent-main-business) <br>
- [Publisher profile](https://clawhub.ai/user/daviddatamining) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API calls, Guidance] <br>
**Output Format:** [Markdown report with tables, sourced fields, and concise narrative analysis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a company name or enterprise ID; may pause for user confirmation when multiple matching companies are returned.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
