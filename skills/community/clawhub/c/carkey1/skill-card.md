## Description: <br>
CarKey lets an agent query a vehicle's location and status, including locks, doors, windows, air conditioning, and power state, on Linux, macOS, or Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkisme](https://clawhub.ai/user/lkisme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent check an authenticated vehicle's current location and condition from natural-language requests such as asking where the vehicle is or whether it is locked. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle API tokens are stored locally and could expose vehicle access if the cache file is copied or read by another user. <br>
Mitigation: Use the skill only on trusted machines, restrict or delete ~/.carkey_cache.json after use, and rotate or revoke vehicle tokens if the file may have been exposed. <br>
Risk: Recent location query history is stored locally and may reveal sensitive vehicle movement or address information. <br>
Mitigation: Avoid shared or unmanaged devices and delete ~/.carkey_history.json when the location history is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lkisme/carkey1) <br>
- [Git for Windows](https://git-scm.com/download/win) <br>
- [Vehicle API base URL](https://openapi.nokeeu.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Terminal text output with shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq; uses cached vehicleToken and accessToken values to query vehicle condition and position.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
