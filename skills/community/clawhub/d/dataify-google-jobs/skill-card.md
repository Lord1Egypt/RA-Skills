## Description: <br>
Turns a user's Google Jobs search request into a Dataify Scraper API form POST and returns the raw API response. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to search Google Jobs through Dataify, review the complete request parameters before execution, and return the original job-search response for downstream use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Job-search parameters are sent to an external Dataify jobs API. <br>
Mitigation: Confirm that the search terms and location fields are acceptable to share before approving the API call. <br>
Risk: The confirmation table may use Chinese labels, which can make parameter review harder for non-Chinese users. <br>
Mitigation: Review each displayed value carefully before confirmation and ask for changes when any field is unclear. <br>
Risk: Job searches can include unnecessary personal or private details. <br>
Mitigation: Avoid entering private personal information unless it is required for the search. <br>


## Reference(s): <br>
- [Dataify Google Jobs API reference](references/google_jobs_api.md) <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-google-jobs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown parameter confirmation table followed by the raw Dataify API response body.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user confirmation before API calls and avoids summarizing or reformatting the returned response.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
