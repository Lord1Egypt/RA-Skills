## Description: <br>
Connect to the Anycast agent network to list agents, query cross-environment connectors, send messages to remote agents, and check fleet status. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[markspeed](https://clawhub.ai/user/markspeed) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to interact with an Anycast tenant from an assistant, including listing fleet agents, querying configured connectors, sending remote-agent messages, checking fleet statistics, and managing tenant-scoped memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send messages or commands to remote agents and query configured connectors. <br>
Mitigation: Use a least-privilege Anycast token and confirm remote-agent messages or connector queries before use in sensitive environments. <br>
Risk: Connector queries, messages, and memory values may expose secrets, personal data, or other sensitive tenant information. <br>
Mitigation: Avoid sending secrets or personal data through messages, connector queries, or tenant-scoped memory values. <br>


## Reference(s): <br>
- [Anycast agent portal](https://agents.anycast.com) <br>
- [ClawHub skill page](https://clawhub.ai/markspeed/anycast-network) <br>
- [Publisher profile](https://clawhub.ai/user/markspeed) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Connector query results should be formatted as markdown tables; agent lists should show name, status, and last seen time.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
