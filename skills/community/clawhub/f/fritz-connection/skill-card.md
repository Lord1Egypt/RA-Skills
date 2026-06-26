## Description: <br>
Dieser Skill ermöglicht die Abfrage von Statusinformationen und die Steuerung einer AVM FRITZ!Box über die TR-064 Schnittstelle. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wolf128058](https://clawhub.ai/user/wolf128058) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and network administrators use this skill to inspect FRITZ!Box router status, traffic, connected devices, WLAN state, and call history, and to run router control actions such as reconnect, reboot, and WLAN toggles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive FRITZ!Box credentials and private router, connected-device, WLAN, and call-history data. <br>
Mitigation: Protect the .env file, limit access to trusted agents and users, and avoid exposing command output where network or call details should remain private. <br>
Risk: Reconnect, reboot, and WLAN on/off actions can disrupt internet, WLAN, and telephony service for all users on the network. <br>
Mitigation: Require explicit confirmation naming the exact action before running reconnect, reboot, or WLAN toggles. <br>
Risk: Unpinned dependencies can change behavior over time. <br>
Mitigation: Pin and review Python dependencies before deployment when reproducibility or change control is required. <br>


## Reference(s): <br>
- [Fritz Connection ClawHub release](https://clawhub.ai/wolf128058/fritz-connection) <br>
- [fritzconnection documentation](https://fritzconnection.readthedocs.io/) <br>
- [fritzconnection GitHub repository](https://github.com/kbr/fritzconnection) <br>
- [AVM TR-064 interfaces](https://avm.de/service/schnittstellen/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include router status, device lists, traffic summaries, WLAN state, call history, and safety prompts for disruptive actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
