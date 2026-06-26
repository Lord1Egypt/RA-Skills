## Description: <br>
Queries a user's vehicle location and condition, including lock, door, window, climate, power, and other status fields. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lkisme](https://clawhub.ai/user/lkisme) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Vehicle owners or agents assisting them use this skill to query where a vehicle is and check whether key status items such as locks, doors, windows, power, and climate are in the expected state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles vehicle access tokens and may leave credentials or vehicle-location history in local plaintext cache files. <br>
Mitigation: Install only when the publisher and vehicle API provider are trusted, treat vehicleToken and accessToken like passwords, avoid shared machines, and remove ~/.carkey_cache.json and ~/.carkey_history.json after use when local retention is not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lkisme/carkey) <br>
- [Vehicle API base URL](https://openapi.nokeeu.com) <br>
- [Git for Windows](https://git-scm.com/download/win) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance] <br>
**Output Format:** [Terminal text and Markdown-style instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return vehicle location and condition details from the configured vehicle API.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
