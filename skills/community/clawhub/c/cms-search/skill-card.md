## Description: <br>
Searches the web through a CMS search service and returns current internet results as JSON or Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spzwin](https://clawhub.ai/user/spzwin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to route web and current-information queries through a CMS search service. It can select a source channel, include an optional query datetime, and return either raw JSON or a Markdown summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to a third-party CMS search service. <br>
Mitigation: Avoid sensitive search terms unless the service is trusted and CMS_USER_KEY is controlled by the deploying organization. <br>
Risk: The skill is designed to route broad online and current-information requests through its external service by default. <br>
Mitigation: Install it only for deployments that intentionally use this CMS search provider, and review returned results before relying on them. <br>
Risk: Time-sensitive searches may assume Asia/Shanghai time. <br>
Mitigation: Provide an explicit datetime and timezone context when freshness or local timing matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/spzwin/cms-search) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [JSON object or Markdown text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CMS_USER_KEY; optional source and datetime parameters can influence the search channel and time context.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
