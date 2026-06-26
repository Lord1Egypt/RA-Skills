## Description: <br>
Agent ID helps agents create a persistent cross-platform identity by generating an identity card, emitting OADP discovery signals, and registering on open coordination hubs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to make an agent discoverable across sessions by adding OADP metadata, registering with a coordination hub, and preparing identity details for other agents to find. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Publishing agent identity details and endpoints can expose operational profile information outside the local session. <br>
Mitigation: Use non-sensitive names, descriptions, and capabilities, and avoid private endpoints or secrets in registration fields. <br>
Risk: Saved ClawSwarm credentials could be exposed if the local credentials file is mishandled. <br>
Mitigation: Protect ~/.config/clawswarm/credentials.json and review local file permissions before use. <br>
Risk: The skill points users to third-party endpoints and companion skills for discovery and registration. <br>
Mitigation: Review the ClawSwarm endpoints and any companion skills, such as agent-ping or clawswarm, separately before installing or registering. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/imaflytok/agent-id) <br>
- [Publisher Profile](https://clawhub.ai/user/imaflytok) <br>
- [ClawSwarm OADP Hub Endpoint](https://onlyflies.buzz/clawswarm/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes external discovery and registration endpoints; users should supply non-sensitive identity details.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
