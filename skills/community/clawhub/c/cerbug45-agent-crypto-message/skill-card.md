## Description: <br>
Enables AI agents to communicate securely with each other through encrypted messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to create encrypted agent-to-agent messaging workflows for coordination, data sharing, and asynchronous collaboration across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports that agent identities, message metadata, encrypted queued messages, attachments, channels, logs, and an unencrypted private key may be stored under /home/claude/.clawhub. <br>
Mitigation: Install only when that local storage model is acceptable; add encrypted key storage, retention limits, and cleanup procedures before handling sensitive data. <br>
Risk: The security evidence advises using the skill only with trusted recipients and low-sensitivity data unless stronger controls are added. <br>
Mitigation: Restrict use to trusted recipients, verify recipient identities, and add authenticated recipient verification before exchanging higher-sensitivity content. <br>
Risk: The security evidence calls out broad data-sharing behavior around attachments, channels, and queued messages. <br>
Mitigation: Apply file-attachment limits, message retention controls, and review procedures for shared data before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cerbug45/cerbug45-agent-crypto-message) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Python and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may result in local identity, queue, registry, channel, attachment, and log files under /home/claude/.clawhub.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
