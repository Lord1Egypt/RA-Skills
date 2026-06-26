## Description: <br>
Manage multiple communication channels, admin identity recognition, and primary channel configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MontyCN](https://clawhub.ai/user/MontyCN) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and operators use this skill to recognize the admin across communication channels, manage trusted contacts, configure a primary notification channel, and route proactive messages or escalations to the right place. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect admin or channel identity could route operational updates to the wrong recipient. <br>
Mitigation: Verify that only the real admin can DM the agent and confirm channel IDs carefully before setting a primary channel. <br>
Risk: Primary-channel and trusted-contact files contain sensitive routing and trust decisions. <br>
Mitigation: Protect and periodically review ~/primary-channel.json and ~/trusted-contacts.json. <br>
Risk: Sensitive notifications may pass through third-party communication providers. <br>
Mitigation: Avoid routing sensitive operational updates through providers the operator does not trust. <br>


## Reference(s): <br>
- [Channel Management Skill Page](https://clawhub.ai/MontyCN/channel-management) <br>
- [MontyCN Publisher Profile](https://clawhub.ai/user/MontyCN) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes file-based channel state and trusted-contact workflows for an agent to follow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
