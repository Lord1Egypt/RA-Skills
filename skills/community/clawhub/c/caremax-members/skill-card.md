## Description: <br>
Manage family member profiles in CareMax Health for listing members, switching profiles, and scoping health data queries to a selected family member. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kittenyang](https://clawhub.ai/user/kittenyang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
CareMax Health users and their agents use this skill to list family members and select a member profile before retrieving or showing member-specific health data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retrieve or display sensitive family health records for non-default members. <br>
Mitigation: Use it only when authorized for the relevant family member and confirm the intended member before showing member-specific medical data. <br>
Risk: The skill depends on the separate caremax-auth package and may start an authentication flow when credentials are missing. <br>
Mitigation: Install and trust caremax-auth before use, review how it stores credentials, and confirm authentication behavior before running the skill. <br>


## Reference(s): <br>
- [CareMax Members on ClawHub](https://clawhub.ai/kittenyang/caremax-members) <br>
- [Publisher profile: kittenyang](https://clawhub.ai/user/kittenyang) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and API request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the sibling caremax-auth skill for authenticated CareMax API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
