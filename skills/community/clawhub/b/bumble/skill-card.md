## Description: <br>
Bumble session, auth, matches, messages, sending, and profile-photo export via Remote Browser Service for an operator's own Bumble web account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vasyaod](https://clawhub.ai/user/vasyaod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to operate their own Bumble web session through a trusted Remote Browser Service, including inspecting state, listing matches, reading or sending permitted messages, and exporting profile photos. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform sensitive Bumble account actions, including auth, sending messages, unmatching, location changes, debugging, and photo export. <br>
Mitigation: Use it only with the operator's own Bumble account and explicitly approve each sensitive action before execution. <br>
Risk: The Remote Browser Service can observe Bumble activity and may store or access the active session. <br>
Mitigation: Use only a trusted Remote Browser Service and clear or log out of the stored session when finished. <br>
Risk: The skill automatically changes the account location to San Francisco after session start. <br>
Mitigation: Confirm that the location change is acceptable before running session actions. <br>


## Reference(s): <br>
- [ClawHub Bumble skill page](https://clawhub.ai/vasyaod/bumble) <br>
- [Bumble web app](https://bumble.com/app) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Files, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands; command outputs are JSON or downloaded image files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires operator-supplied phone/SMS inputs and trusted Remote Browser Service access.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
