## Description: <br>
CFM Redis provides Redis Pub/Sub-based real-time communication for agents across frameworks while reducing unnecessary polling-related token use. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ameylover](https://clawhub.ai/user/ameylover) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to set up Redis-backed messaging, message history, and agent discovery for cross-framework multi-agent collaboration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Redis retains recent inter-agent messages, so stored message contents may contain sensitive data. <br>
Mitigation: Keep Redis local or authenticated, avoid sending secrets through CFM, and periodically purge message history when retention is not needed. <br>
Risk: Forwarding messages to webhooks can expose message content outside the local Redis environment. <br>
Mitigation: Disable webhook forwarding unless required, and tightly control any configured webhook endpoint. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ameylover/cfm-redis) <br>
- [Publisher profile](https://clawhub.ai/user/ameylover) <br>
- [Project homepage](https://github.com/AmeyLover/cfm-redis) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires redis-server, python3, and the redis Python package.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
