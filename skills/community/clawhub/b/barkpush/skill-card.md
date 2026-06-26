## Description: <br>
Sends Bark notifications with multi-user targeting, content-type detection, history tracking, and message update support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liberalchang](https://clawhub.ai/user/liberalchang) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and automation users use barkpush to send text, link, image, and alert notifications through a configured Bark server to one or more users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notification content and Bark device identifiers may be sent to the configured Bark server. <br>
Mitigation: Use only trusted Bark server endpoints and avoid sending sensitive content unless that delivery path is acceptable. <br>
Risk: Device keys, ciphertext, and push history can be stored in local configuration or state files. <br>
Mitigation: Keep secrets out of shared repositories, prefer environment variables for sensitive values, and protect the .bark-push state directory. <br>
Risk: All-user pushes and delete commands can affect multiple recipients or prior notifications. <br>
Mitigation: Review target users and command mode before running broad delivery, update, or delete actions. <br>


## Reference(s): <br>
- [Bark Official Website](https://bark.day.app) <br>
- [Bark API Documentation](https://bark.day.app/#/tutorial) <br>
- [ClawHub Skill Page](https://clawhub.ai/liberalchang/barkpush) <br>
- [Usage Guide](artifact/docs/usage.md) <br>
- [Architecture Notes](artifact/docs/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Plain text status messages with command-line arguments and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send notification payloads to the configured Bark server and store local push history.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
