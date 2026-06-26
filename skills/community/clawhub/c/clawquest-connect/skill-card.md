## Description: <br>
Connects Claw Quest Android to an OpenClaw gateway using the manual URL-and-token flow, with optional WhatsApp handoff and one-time approval of a matching Android pairing request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sandrokitchener](https://clawhub.ai/user/sandrokitchener) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to send the gateway URL plus the required token or password to Claw Quest Android and approve one matching device-pair request when pairing reaches the gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles live OpenClaw gateway credentials and may send them through WhatsApp or chat. <br>
Mitigation: Use it only while pairing a device you control, confirm the WhatsApp destination first, and rotate the gateway secret if details are sent unexpectedly. <br>
Risk: The skill can approve a pending Android pairing request with operator-level access. <br>
Mitigation: Approve only the next request that matches Claw Quest Android and revoke the paired device if any approval is unexpected. <br>


## Reference(s): <br>
- [Claw Quest Connect on ClawHub](https://clawhub.ai/sandrokitchener/clawquest-connect) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and concise status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include the gateway URL and one active token or password needed for manual pairing when configured.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
