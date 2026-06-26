## Description: <br>
Controls AVM FRITZ!Box routers and FRITZ!DECT smart-home devices via TR-064 and the Homeautoswitch API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[first-it-consulting](https://clawhub.ai/user/first-it-consulting) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent inspect and manage a local FRITZ!Box router, Wi-Fi state, connected devices, internet reconnects, and paired FRITZ!DECT smart-home devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Router, Wi-Fi, reconnect, and smart-home commands can change network availability or physical device state. <br>
Mitigation: Require explicit user confirmation before Wi-Fi changes, internet reconnects, or smart-home switch and toggle operations. <br>
Risk: FRITZ!Box credentials grant access to router and smart-home actions supported by the configured account. <br>
Mitigation: Use a dedicated least-privilege FRITZ!Box user and store credentials in a protected .env file instead of command-line arguments. <br>
Risk: A misconfigured host could direct the skill away from the intended local router. <br>
Mitigation: Verify FRITZBOX_HOST points to the user's own local FRITZ!Box before use. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/first-it-consulting/fritzbox) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/first-it-consulting) <br>
- [README](README.md) <br>
- [Installation Guide](INSTALL.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and plain-text command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May run local router and smart-home control commands when configured with FRITZ!Box credentials and host settings.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
