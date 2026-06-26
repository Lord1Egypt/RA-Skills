## Description: <br>
X/Twitter integration for posting, replying, searching, liking, following, direct messages, and mentions via the official X API v2. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xonder](https://clawhub.ai/user/xonder) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use Clawbird to let an agent read from and act through an X/Twitter account via the official X API v2. Typical tasks include posting tweets and replies, searching recent tweets, retrieving profiles and mentions, sending direct messages, and tracking estimated API cost. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can post, reply, like, follow, and send direct messages through the user's X account. <br>
Mitigation: Require explicit confirmation for write actions and use a dedicated or least-privileged X app for agent access. <br>
Risk: X API credentials grant sensitive account access if exposed or used with unreviewed runtime code. <br>
Mitigation: Provide credentials only through runtime plugin configuration or environment variables, and pin or review the npm package before granting credentials. <br>
Risk: Mutation actions are recorded in a local session interaction log. <br>
Mitigation: Review the log for accountability and delete it when local retention of account activity is not desired. <br>


## Reference(s): <br>
- [Clawbird on ClawHub](https://clawhub.ai/xonder/clawbird) <br>
- [Publisher profile](https://clawhub.ai/user/xonder) <br>
- [npm package @xonder/clawbird](https://www.npmjs.com/package/@xonder/clawbird) <br>
- [X Developer Portal](https://developer.x.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API Calls, Text, Guidance] <br>
**Output Format:** [JSON tool results with IDs, URLs, profile or tweet data, estimated API costs, and error objects when operations fail.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Mutation tools can create remote X account actions and a session-scoped local interaction log; X API credentials are required at runtime.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
