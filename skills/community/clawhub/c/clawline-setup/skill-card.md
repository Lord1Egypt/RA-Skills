## Description: <br>
ClawLine Setup helps an OpenClaw agent install the ClawLine channel plugin, bind a phone UUID, check connection status, and disconnect an existing pairing through conversation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qtx0213](https://clawhub.ai/user/qtx0213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to configure ClawLine mobile app connectivity without manually running setup commands. It supports plugin installation, phone UUID pairing, status checks, and disconnection workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Using the skill may install executable plugin code from the ClawLine package. <br>
Mitigation: Install only when the user trusts the ClawLine project and the @openclawline/clawline-setup package. <br>
Risk: Updating the phone UUID may replace an existing pairing or disconnect a previously connected device. <br>
Mitigation: Confirm the intended device UUID and current pairing before updating or clearing connection settings. <br>
Risk: Restarting the OpenClaw gateway can interrupt active OpenClaw service. <br>
Mitigation: Run setup or rebinding when a brief gateway restart is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qtx0213/clawline-setup) <br>
- [ClawLine App](https://openclawline.com) <br>
- [npm package @openclawline/clawline-setup](https://www.npmjs.com/package/@openclawline/clawline-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with conversational setup guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install plugin code, update or clear phone UUID pairing, restart the OpenClaw gateway, and report connection status.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
