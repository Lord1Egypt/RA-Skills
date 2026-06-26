## Description: <br>
Optional helper skill for Boktoshi human /my endpoints that require Firebase ID token auth. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rsmfc](https://clawhub.ai/user/rsmfc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to access Boktoshi human account /my endpoints, such as profile, positions, and activity, when a valid Firebase ID token is available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses FIREBASE_ID_TOKEN for authenticated Boktoshi account access, and token exposure could compromise the account. <br>
Mitigation: Provide the token only in trusted environments, treat it like a password, and avoid storing it in public logs, prompts, or transcripts. <br>
Risk: The skill is scoped to human account /my endpoints and may access personal account data. <br>
Mitigation: Use it only where human session context is required and verify that requests are limited to the intended /my endpoints. <br>


## Reference(s): <br>
- [Boktoshi API base URL](https://boktoshi.com/api/v1) <br>
- [ClawHub skill page](https://clawhub.ai/rsmfc/boktoshi-human-helper) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown guidance with HTTP endpoint and authorization header details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires FIREBASE_ID_TOKEN and network access to the Boktoshi API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill body) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
