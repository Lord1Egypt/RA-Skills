## Description: <br>
Everclaw provides encrypted cloud backup and restore for an agent's memory, identity, profile, and workspace configuration files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tlxue](https://clawhub.ai/user/tlxue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Everclaw to preserve agent memory and identity across devices, reinstalls, and workspace resets by syncing selected local files to a remote vault. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can upload agent memory, identity, user profile, TOOLS.md, and HEARTBEAT.md files to a third-party service. <br>
Mitigation: Review synced files for secrets or sensitive details before invoking the skill, and only install it if third-party storage of those files is acceptable. <br>
Risk: The artifact configures recurring sync behavior without a clear consent step. <br>
Mitigation: Confirm recurring sync is desired before enabling the skill and periodically review HEARTBEAT.md and OpenClaw configuration for Everclaw sync entries. <br>
Risk: Exposure of EVERCLAW_API_KEY could allow access to the vault. <br>
Mitigation: Protect the API key, avoid logging or displaying it, and rotate or reprovision it if exposure is suspected. <br>


## Reference(s): <br>
- [Everclaw ClawHub listing](https://clawhub.ai/tlxue/everclaw) <br>
- [Publisher profile: tlxue](https://clawhub.ai/user/tlxue) <br>
- [Everclaw service endpoint](https://everclaw.chong-eae.workers.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with bash command snippets, JSON API responses, and configuration/file update instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local OpenClaw configuration, HEARTBEAT.md, and selected memory or identity files during sync workflows.] <br>

## Skill Version(s): <br>
0.3.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
