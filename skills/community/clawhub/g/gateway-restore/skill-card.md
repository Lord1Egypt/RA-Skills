## Description: <br>
Restore a gateway to its last known-good configuration, or tag the current config as known-good when a gateway configuration change needs fast rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halfdeadcat](https://clawhub.ai/user/halfdeadcat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to restore Slack or Discord gateway configuration from a known-good backup, tag current configuration as known-good, and restart the gateway with health checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can overwrite live Slack or Discord gateway configuration and restart services. <br>
Mitigation: Install it only on gateway hosts you operate, review the local restart scripts before use, and keep known-good backups current. <br>
Risk: Broad natural-language restore requests can trigger rollback behavior without enough confirmation or scoping. <br>
Mitigation: Require an explicit target gateway and confirmation before production restores; prefer scoped commands such as /restore slack or /restore discord. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/halfdeadcat/gateway-restore) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and operational status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local shell scripts that copy gateway configuration files, create backups, and restart Slack or Discord gateway services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
