## Description: <br>
Submit Dataify Facebook Profile by Profile URL Builder tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dataify-server](https://clawhub.ai/user/dataify-server) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit Dataify Builder jobs that collect Facebook personal profile data by profile URL and return the resulting task ID and status. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Dataify API TOKEN to submit Builder jobs. <br>
Mitigation: Store DATAIFY_API_TOKEN like any other API credential and do not submit a Builder request without an intended token. <br>
Risk: Submitted Facebook profile URLs are sent to Dataify and may be processed or billed under the user's account. <br>
Mitigation: Check the target Facebook URL and confirm the user intends to submit the Dataify collection task before approving submission. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dataify-server/dataify-facebook-profile-by-url) <br>
- [Dataify dashboard](https://dashboard.dataify.com?utm_source=skill) <br>
- [Dataify login](https://dashboard.dataify.com/login?utm_source=skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration guidance, JSON] <br>
**Output Format:** [Markdown guidance with optional shell commands and JSON task summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Submissions require a Dataify API TOKEN and a Facebook profile URL.] <br>

## Skill Version(s): <br>
1.1.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
