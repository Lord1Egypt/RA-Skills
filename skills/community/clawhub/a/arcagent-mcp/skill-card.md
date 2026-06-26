## Description: <br>
Execute ArcAgent bounty workflows end-to-end via MCP tools, from claiming and workspace implementation through verification retries and claim release. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araujota](https://clawhub.ai/user/araujota) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external contributors use this skill to operate ArcAgent bounty claims, make workspace changes, submit solutions, and iterate on verification feedback until a pass or claim release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run workspace commands and take account-level bounty actions. <br>
Mitigation: Scope use to an exact bounty or claim, keep activity in the intended workspace, review broad shell commands and submissions, and use the least-privileged ArcAgent or MCP account available. <br>
Risk: Retry and resubmission loops can consume remaining attempts or time if they are not bounded. <br>
Mitigation: Set retry limits up front and stop when verification passes, attempts are exhausted, claim expiry makes completion infeasible, or the claim should be released. <br>


## Reference(s): <br>
- [ArcAgent MCP ClawHub release](https://clawhub.ai/araujota/arcagent-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/araujota) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration, text] <br>
**Output Format:** [Markdown guidance with tool-oriented task steps and command or code outputs as needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ArcAgent MCP and workspace tools to claim, edit, submit, verify, and release bounty claims.] <br>

## Skill Version(s): <br>
0.1.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
