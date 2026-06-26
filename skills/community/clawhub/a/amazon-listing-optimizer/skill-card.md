## Description: <br>
Analyze Amazon product listings, score listing quality, find keyword opportunities, and compare competitors without API keys or subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avmw2025](https://clawhub.ai/user/avmw2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers, ecommerce operators, and listing optimization agents use this skill to evaluate Amazon ASIN listing quality, discover autocomplete keyword opportunities, and identify competitor listings to study before improving product pages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes Amazon web requests using ASINs, marketplace domains, or search terms supplied by the user. <br>
Mitigation: Run it only with product identifiers and search terms that are appropriate to send to Amazon, and review network behavior before deployment in restricted environments. <br>
Risk: The skill saves generated analysis and keyword research reports under its reports folder. <br>
Mitigation: Review saved reports for sensitive product research data and remove or control access to files that should not be shared. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/avmw2025/amazon-listing-optimizer) <br>
- [Publisher profile](https://clawhub.ai/user/avmw2025) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and locally saved JSON reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Report files are saved under the skill reports folder when scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
