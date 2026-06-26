## Description: <br>
aigame lets an agent play a five-chapter reasoning adventure over HTTP, testing inference, memory, calculation, and decision-making. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[val1813](https://clawhub.ai/user/val1813) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent register a temporary game session, call the remote AgentWorld API, and narrate progress through a reasoning adventure game. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts 111.231.112.127 over unencrypted HTTP. <br>
Mitigation: Use it only when that network contact is acceptable, and avoid sending sensitive information through the game dialogue. <br>
Risk: The skill creates a temporary game account and receives game tokens. <br>
Mitigation: Use a non-personal nickname and treat returned tokens as temporary secrets. <br>
Risk: User-invocable game triggers can start remote API interaction accidentally. <br>
Mitigation: Install only in environments where the listed game triggers and remote gameplay behavior are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/val1813/aigame) <br>
- [Publisher profile](https://clawhub.ai/user/val1813) <br>
- [AgentWorld game API base](http://111.231.112.127:9000) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown narrative with inline bash commands and summarized API results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Contacts a remote HTTP game API and may handle temporary game tokens returned by that service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
