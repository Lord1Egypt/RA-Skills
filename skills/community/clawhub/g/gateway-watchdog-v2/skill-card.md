## Description: <br>
Production-grade bash watchdog for the OpenClaw gateway that runs via launchd every 5 minutes and uses boot grace, retry backoff, port checks, stale PID detection, and restart cooldowns to avoid restart loops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BryanTegomoh](https://clawhub.ai/user/BryanTegomoh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install or run a macOS watchdog that monitors the local OpenClaw gateway and restarts it when health checks, retries, and cooldown checks indicate it is stale or unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The watchdog is a persistent macOS background task that can restart the local OpenClaw gateway. <br>
Mitigation: Install it only when that behavior is intended, verify the script path before loading the plist, keep an unload or removal command available, and monitor ~/.openclaw/logs/watchdog.log for unexpected restarts. <br>
Risk: An incorrect launchd label, port, or local environment could cause failed checks or unnecessary restart attempts. <br>
Mitigation: Confirm the gateway runs under ai.openclaw.gateway on macOS, that curl and lsof are available, and that the gateway listens on 127.0.0.1:18789 before scheduling the watchdog. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/BryanTegomoh/gateway-watchdog-v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and launchd plist configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup guidance and a bash watchdog script for macOS launchd.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
