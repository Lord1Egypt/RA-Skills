## Description: <br>
Query public holidays for a country and year using the apipick Public Holidays API, returning sorted holiday dates and official names. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[javainthinking](https://clawhub.ai/user/javainthinking) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to list public holidays, check whether a date is a public holiday, or plan around holidays for supported countries and years. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent sends country and year holiday lookups to apipick using the user's APIPICK_API_KEY. <br>
Mitigation: Configure the API key through the environment or an approved secrets mechanism, and avoid pasting secrets into chat. <br>
Risk: Successful requests may consume apipick API credits. <br>
Mitigation: Monitor API credit usage and confirm the intended country and year before making repeated requests. <br>


## Reference(s): <br>
- [apipick Public Holidays API Reference](references/api_reference.md) <br>
- [apipick API Platform](https://www.apipick.com) <br>
- [apipick Public Holidays](https://www.apipick.com/public-holidays) <br>
- [ClawHub Skill Page](https://clawhub.ai/javainthinking/apipick-public-holidays) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown text with optional shell commands and JSON API response summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires APIPICK_API_KEY and may consume one apipick credit per successful API request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
