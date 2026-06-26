## Description: <br>
Queries DAO3 platform data by user ID, map ID, keyword, or authenticated account context, returning profiles, map details, comments, favorites, recent plays, messages, statistics, retention, behavior data, and raw endpoint responses as JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ifishcool](https://clawhub.ai/user/ifishcool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch DAO3 public data and authenticated account or map statistics through a Python command-line interface. It is useful for DAO3 user, map, message, and analytics lookup workflows where JSON output is expected. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make authenticated DAO3 API requests, including broad raw endpoint requests beyond the named query commands. <br>
Mitigation: Use a minimally scoped DAO3 token when available, avoid passing secrets directly on the command line, and call raw endpoints only after confirming the exact DAO3 path and account data involved. <br>


## Reference(s): <br>
- [DAO3 API base endpoint](https://code-api-pc.dao3.fun) <br>
- [ClawHub skill page](https://clawhub.ai/ifishcool/dao3-statistics) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Guidance] <br>
**Output Format:** [JSON emitted by Python CLI commands, with Markdown guidance for command usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Authenticated commands require a DAO3 token and user-agent; failures are returned as JSON objects with error details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
