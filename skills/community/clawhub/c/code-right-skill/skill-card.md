## Description: <br>
Code Right Skill creates software copyright application material generation tasks by sending a system name and notification email to softcraft.cloud, which prepares formatted documents, screenshots, ZIP packaging, and email delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziyiyu](https://clawhub.ai/user/ziyiyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to start software copyright registration material generation for a named system and receive the completed package by email. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the software or system name, recipient email, generated documents, and any optional access token to softcraft.cloud. <br>
Mitigation: Install and use the skill only when softcraft.cloud is trusted for those materials and credentials. <br>
Risk: A mistyped notification email could expose confidential business or legal materials to the wrong recipient. <br>
Mitigation: Confirm the destination email before creating a task, especially for confidential materials. <br>
Risk: The workflow depends on the remote softcraft.cloud service being available. <br>
Mitigation: Confirm softcraft.cloud is reachable before relying on the skill for time-sensitive document generation. <br>


## Reference(s): <br>
- [Code Right Skill on ClawHub](https://clawhub.ai/ziyiyu/code-right-skill) <br>
- [Softcraft Cloud](https://softcraft.cloud) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [JSON task creation response from a remote service, with generated Word documents and ZIP delivery handled by email.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a system name and notification email; an access token is optional for filtering and download authorization.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata, target metadata, and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
