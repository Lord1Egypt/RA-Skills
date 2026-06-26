## Description: <br>
Handle China Mobile Digital Credential authorization flow for sensitive operations by loading app credentials, binding an agent, requesting user authorization, polling authorization status, and verifying approval before proceeding. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[riceankim](https://clawhub.ai/user/riceankim) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to gate sensitive agent actions with CMCC Digital Credential authorization. It supports credential setup, agent binding, authorization-link generation, and polling before the agent proceeds with a protected operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable app credentials and can expose appKey data through credential retrieval workflows. <br>
Mitigation: Use limited-scope credentials, avoid displaying appKey values, protect or delete memory/cmcc-digital-credential.json after use, and rotate the key if it appears in logs. <br>
Risk: The authorization flow handles phone-number data through the CMCC authorization service. <br>
Mitigation: Confirm that sending the phone number to the CMCC authorization service is acceptable for the intended use case before enabling the workflow. <br>
Risk: The workflow depends on a CMCC test endpoint and a third-party publisher. <br>
Mitigation: Install only when the publisher and CMCC test endpoint are trusted for the deployment context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/riceankim/cmcc-credential) <br>
- [CMCC test authorization endpoint](https://vctest.cmccsign.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local credential state to memory/cmcc-digital-credential.json and call CMCC authorization endpoints when the user authorizes that flow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
