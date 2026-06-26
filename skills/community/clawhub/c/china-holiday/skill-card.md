## Description: <br>
China Holiday identifies mainland China statutory holidays, weekends, adjusted workdays, and school vacation periods for supported cities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[violin](https://clawhub.ai/user/violin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use China Holiday to answer whether a mainland China date is a holiday or workday, list annual holidays, and query school vacation periods for supported cities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The unpinned chinese-calendar dependency can resolve to future upstream releases with changed behavior. <br>
Mitigation: Install chinese-calendar from a trusted package source and pin a reviewed version for repeatable or production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/violin/china-holiday) <br>
- [Publisher profile](https://clawhub.ai/user/violin) <br>
- [Dependency declaration](requirements.txt) <br>
- [Supported city vacation configuration](config/regions.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Code, Configuration] <br>
**Output Format:** [Plain text command output and Python function return values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Python 3 and the chinese-calendar package.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
