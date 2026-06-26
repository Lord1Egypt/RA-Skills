## Description: <br>
Sends an email via Gmail when a message starts with "cma" or "cmap". <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mtbf999](https://clawhub.ai/user/mtbf999) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Users can trigger outbound Gmail messages to predefined recipients by starting a request with the cma or cmap prefix and supplying a subject and body. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Short cma and cmap triggers can cause accidental or prompt-injected outbound email. <br>
Mitigation: Add an explicit confirmation step that displays the recipient, subject, and body before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mtbf999/cma-email) <br>
- [Publisher profile](https://clawhub.ai/user/mtbf999) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Text instructions and a Gmail send command] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the gog skill to send Gmail messages to predefined recipients.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
