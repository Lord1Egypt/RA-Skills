## Description: <br>
ClawMe sends user-confirmed browser automation instructions through a Chrome extension so agents can fill forms, compose messages, click controls, open URLs, extract page text, and create reminders in the user's existing Chrome session. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongsheng123132](https://clawhub.ai/user/dongsheng123132) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use ClawMe to let an agent propose browser actions such as filling forms, composing messages, clicking controls, opening URLs, extracting page text, and creating reminders in the user's existing Chrome session after user confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose actions in logged-in browser sessions, including posts, submissions, clicks, and extraction from private pages. <br>
Mitigation: Review every side-panel action before approval and avoid approving sensitive submissions, public posts, payments, or private-page extraction unless the user is comfortable with the action and data handling. <br>
Risk: Use depends on trust in the ClawMe Chrome extension and service handling browser instructions and any extracted content. <br>
Mitigation: Install and use the skill only when the user trusts the ClawMe extension and service, and limit instructions that include sensitive data. <br>


## Reference(s): <br>
- [ClawMe ClawHub release page](https://clawhub.ai/dongsheng123132/clawme) <br>
- [ClawMe API base URL](https://api.clawme.net) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON instruction payloads, Configuration guidance] <br>
**Output Format:** [Markdown guidance with HTTP request examples and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWME_CLIENT_TOKEN and a configured ClawMe Chrome extension; extracted page text may be returned to the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
