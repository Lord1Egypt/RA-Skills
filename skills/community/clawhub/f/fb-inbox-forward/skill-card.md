## Description: <br>
Forwards Facebook Page inbox messages to a configured OpenClaw channel in real time with an opt-in PowerShell listener that avoids writing message content to disk. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seph1709](https://clawhub.ai/user/seph1709) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to forward inbound Facebook Page messages into a chosen OpenClaw channel or target. It is suited for teams that need opt-in, continuous inbox notification while keeping credentials in local config files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Full Facebook Page message text is forwarded to the configured OpenClaw destination. <br>
Mitigation: Confirm the destination is trusted before starting the listener and inform the user that message text, sender name, and conversation ID will be transmitted. <br>
Risk: Facebook Page credentials and forwarding configuration are sensitive local files. <br>
Mitigation: Use a least-privileged Page token, keep config files permission-restricted, and do not commit runtime config files to version control. <br>
Risk: The optional background listener continuously polls and forwards messages until stopped. <br>
Mitigation: Start the listener only after explicit user request and stop it when continuous forwarding is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/seph1709/fb-inbox-forward) <br>
- [Publisher profile](https://clawhub.ai/user/seph1709) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with PowerShell code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, listener control, status, logging, and troubleshooting guidance for forwarding Facebook Page inbox messages through OpenClaw.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata and artifact _meta.json, published 2026-03-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
