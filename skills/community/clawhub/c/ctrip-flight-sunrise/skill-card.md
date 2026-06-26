## Description: <br>
Search and compare flight tickets on Ctrip by departure, arrival, date, and cabin class, returning structured flight and price information in JSON format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andrew-707](https://clawhub.ai/user/andrew-707) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and travel-operations users can invoke this skill to search Ctrip routes, compare dates, identify direct or connecting flights, and export structured flight and price data for downstream analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill bundles and automatically sends a preset browser cookie, and its documentation tells users how to copy a logged-in Ctrip cookie into source code. <br>
Mitigation: Remove the bundled FVP cookie before use. Provide any Ctrip cookie only through a local secret or environment variable, and do not paste personal browser cookies into shared source files. <br>
Risk: Using a Ctrip cookie for flight searches may expose account-linked search activity and route/date preferences to the service. <br>
Mitigation: Use only an account and cookie intended for this workflow, review the account and privacy implications before running searches, and rotate or revoke the cookie when it is no longer needed. <br>


## Reference(s): <br>
- [Ctrip Flights](https://flights.ctrip.com) <br>
- [ClawHub release page](https://clawhub.ai/andrew-707/ctrip-flight-sunrise) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash examples and structured JSON flight-search results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write JSON to a user-specified output path; requires network access to Ctrip and may require a Ctrip FVP cookie.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
