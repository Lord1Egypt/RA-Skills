## Description: <br>
Turns Google Patents search requests into confirmed Dataify Scraper API calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to prepare Google Patents searches, review the resolved parameters, and run the confirmed request through Dataify. It is suited for patent search workflows that need explicit parameter review before sending queries and filters to a third-party API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Patent research queries and filters are sent to Dataify when the API call is approved. <br>
Mitigation: Review the confirmation table before approving each request and avoid sending sensitive searches unless Dataify use is acceptable. <br>
Risk: API tokens can be exposed if pasted into chat or echoed in command output. <br>
Mitigation: Prefer DATAIFY_API_TOKEN from the environment and do not include Authorization in the pre-call parameter table. <br>


## Reference(s): <br>
- [Dataify Google Patents API Reference](references/google_patents_api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/dataify-server/dataify-google-patents) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/dataify-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown parameter review tables, shell command examples, and raw API response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before API calls and returns the response body without summarization or reshaping.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
