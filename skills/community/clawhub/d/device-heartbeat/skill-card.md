## Description: <br>
Monitors macOS device online status by sending scheduled heartbeat pings to healthchecks.io and checking local or remote heartbeat state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[houziershi](https://clawhub.ai/user/houziershi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Device owners and operators use this skill to install a lightweight heartbeat monitor, inspect local heartbeat status, or query healthchecks.io for remote device availability. It is useful when a device appears unreachable or a user wants ongoing online/offline alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The healthchecks.io ping URL can act like a secret and may create false heartbeat pings if shared in chats or logs. <br>
Mitigation: Treat the full ping URL as sensitive, share only the UUID when possible, and avoid pasting it into shared shells, tickets, or messaging tools. <br>
Risk: The setup script installs a persistent user-level macOS LaunchAgent that continues sending heartbeat pings in the background. <br>
Mitigation: Install it only on devices intended to be monitored, review the LaunchAgent behavior before use, and run the provided uninstall script when monitoring is no longer needed. <br>
Risk: Remote status checks require a healthchecks.io API key. <br>
Mitigation: Use a read-only API key, keep it out of shared logs and command history where practical, and rotate it if exposed. <br>


## Reference(s): <br>
- [Healthchecks Setup Guide](references/healthchecks-setup.md) <br>
- [healthchecks.io](https://healthchecks.io/) <br>
- [ClawHub Skill Page](https://clawhub.ai/houziershi/device-heartbeat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install a user-level macOS LaunchAgent, write local heartbeat logs and state, and call healthchecks.io APIs when the user provides credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
