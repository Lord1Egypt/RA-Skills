## Description: <br>
Install, run, and manage the SOS emergency recovery tool for OpenClaw instances when a bot needs diagnosis, recovery, installation, autofix, rollback, network checks, or Telegram testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robertfarkash29-source](https://clawhub.ai/user/robertfarkash29-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or run SOS recovery commands for OpenClaw hosts when bot gateway health, network connectivity, rollback, or Telegram delivery needs diagnosis or repair. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic recovery can restart services, kill OpenClaw processes, change DNS resolver settings, roll back versions, or reinstall gateway components. <br>
Mitigation: Run it only on OpenClaw hosts you administer, prefer interactive review for risky actions, and keep a current backup before using autofix or nuclear recovery. <br>
Risk: Telegram testing uses the configured bot token to make real Telegram API calls. <br>
Mitigation: Use Telegram testing only when sending a real test message through the configured bot is acceptable. <br>
Risk: Installer flows can write to system paths and remote install examples may encourage fetching scripts over the network. <br>
Mitigation: Prefer the bundled script or a pinned, reviewed release and avoid unattended `curl | bash` installs. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/robertfarkash29-source/claw-sos) <br>
- [Publisher profile](https://clawhub.ai/user/robertfarkash29-source) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include privileged OpenClaw host recovery commands.] <br>

## Skill Version(s): <br>
6.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
