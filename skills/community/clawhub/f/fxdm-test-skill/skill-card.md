## Description: <br>
Manage Trello boards, lists, and cards via the Trello REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fxdm41202425](https://clawhub.ai/user/fxdm41202425) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect Trello boards, lists, and cards and to create, move, comment on, or archive cards through Trello REST API commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Trello token can read and change real boards and cards. <br>
Mitigation: Use the narrowest or most disposable token available and require explicit confirmation before creating, moving, commenting on, or archiving cards. <br>
Risk: Trello API credentials are provided through environment variables. <br>
Mitigation: Keep TRELLO_API_KEY and TRELLO_TOKEN secret, avoid pasting them into logs or shared transcripts, and rotate them if exposure is suspected. <br>
Risk: High-volume use can hit Trello API rate limits. <br>
Mitigation: Throttle repeated requests and handle Trello rate-limit responses before running bulk board, list, or card operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fxdm41202425/fxdm-test-skill) <br>
- [Trello REST API documentation](https://developer.atlassian.com/cloud/trello/rest/) <br>
- [Trello API key page](https://trello.com/app-key) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with curl and jq command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands require jq plus TRELLO_API_KEY and TRELLO_TOKEN environment variables and call Trello REST API endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
