## Description: <br>
Fetch website analytics from Clicky (clicky.com) via their REST API for traffic, visitor, pageview, top page, bounce rate, search ranking, traffic source, country, scheduled report, and date-range comparison requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[djedi](https://clawhub.ai/user/djedi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and analytics users can use this skill to fetch Clicky analytics through shell commands and summarize website traffic, content, SEO, geography, and date-range reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Clicky site ID and site key, which can expose website analytics if mishandled. <br>
Mitigation: Store Clicky credentials in a protected environment file or secret manager, avoid committing environment files, and rotate the key if it appears in logs, screenshots, shell history, or repository files. <br>
Risk: API responses may include analytics data that is sensitive to the site owner. <br>
Mitigation: Install and run the skill only in agent contexts where access to the relevant Clicky analytics account is appropriate. <br>


## Reference(s): <br>
- [Clicky API Data Types](references/api-types.md) <br>
- [Clicky Stats API endpoint](https://api.clicky.com/api/stats/4) <br>
- [ClawHub skill page](https://clawhub.ai/djedi/clicky-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and Clicky site credentials in environment variables.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
