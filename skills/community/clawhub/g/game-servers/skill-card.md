## Description: <br>
Order, configure and manage dedicated game servers (20+ games) via Supercraft REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcjkrs](https://clawhub.ai/user/mcjkrs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to order, inspect, configure, start, stop, restart, and send console commands to dedicated Supercraft game servers through a REST API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can purchase paid game server plans. <br>
Mitigation: Require explicit user approval before creating or opening checkout links. <br>
Risk: The skill can start, stop, restart, reconfigure, and send console commands to servers. <br>
Mitigation: Confirm the target server and requested action before executing operational or destructive changes. <br>
Risk: The skill uses background login polling and stores a JWT for authenticated server control. <br>
Mitigation: Use polling and token storage only when the user approves where the token is stored, how long polling runs, and how to revoke or delete the token. <br>
Risk: The skill can retrieve connection details, including passwords. <br>
Mitigation: Show connection secrets only after explicit user approval and avoid persisting them in logs or shared output. <br>


## Reference(s): <br>
- [Supercraft Agent API Homepage](https://claws.supercraft.host) <br>
- [Getting Started Guide](https://claws.supercraft.host/documentation-for-agents/getting-started.md) <br>
- [OpenAPI Reference](https://claws.supercraft.host/docs) <br>
- [Machine-readable Discovery](https://supercraft.host/llms.txt) <br>
- [ClawHub Skill Page](https://clawhub.ai/mcjkrs/game-servers) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with REST endpoint guidance and inline curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include authenticated server actions, purchase checkout links, login links, connection details, and configuration updates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
