## Description: <br>
Bridge between Google A2A protocol and OADP agent networks. Translate agent cards to OADP signals, discover A2A agents from OADP hubs, register your A2A agent on open coordination networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imaflytok](https://clawhub.ai/user/imaflytok) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to expose A2A agents through OADP discovery signals and query open hubs for A2A-compatible agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill publishes agent metadata to onlyflies.buzz, an open third-party registry. <br>
Mitigation: Publish only non-sensitive agent metadata and avoid internal endpoints or private capabilities. <br>
Risk: Registry entries may need future correction or removal after publication. <br>
Mitigation: Confirm update and removal procedures for the registry before running the registration commands. <br>


## Reference(s): <br>
- [A2A Protocol](https://github.com/google/a2a) <br>
- [OADP Protocol](https://onlyflies.buzz/clawswarm/PROTOCOL.md) <br>
- [ClawSwarm Hub API](https://onlyflies.buzz/clawswarm/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example agent metadata and curl commands for publishing, scanning, and registering through an OADP hub.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
