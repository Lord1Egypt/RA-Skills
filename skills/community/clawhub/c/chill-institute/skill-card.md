## Description: <br>
Use chill.institute through a browser session to search for content, select a result, and send it to put.io. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[baanish](https://clawhub.ai/user/baanish) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to operate the chill.institute web UI, choose an appropriate search result, and start a put.io transfer. It is best paired with a separate putio skill for transfer verification and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use the user's logged-in chill.institute or put.io browser session to start transfers. <br>
Mitigation: Have the agent show the selected result before sending, complete OAuth directly in the browser, do not share passwords in chat, and only run the optional putio verification script if that separate skill is trusted. <br>
Risk: The workflow may be used for content the user is not permitted to access. <br>
Mitigation: Use the workflow only for content the user has rights or permission to access. <br>


## Reference(s): <br>
- [chill.institute sign-in](https://chill.institute/sign-in) <br>
- [ClawHub skill page](https://clawhub.ai/baanish/chill-institute) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands] <br>
**Output Format:** [Markdown with browser workflow steps and inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on the user's existing chill.institute and put.io browser sessions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
