## Description: <br>
Synchronize memory, preferences, and skills between multiple Clawdbot instances over SSH/rsync with Tailscale-supported peer connectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[udiedrichsen](https://clawhub.ai/user/udiedrichsen) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to keep Clawdbot memory, profile state, and selected skill data synchronized across machines they control. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy and overwrite agent memory and profile state across SSH peers. <br>
Mitigation: Use it only between machines you control, run /sync diff before push/pull/sync, and keep backups of synchronized state. <br>
Risk: SSH peer verification is weakened during connection checks. <br>
Mitigation: Use a dedicated least-privilege SSH key/account and pin or verify SSH host keys before syncing. <br>
Risk: Automatic or skill synchronization can propagate unwanted changes after initial setup. <br>
Mitigation: Avoid enabling auto-sync or syncing skills until the workflow has been tested with non-sensitive data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/udiedrichsen/clawdbot-sync) <br>
- [Setup Guide](references/setup.md) <br>
- [Tailscale Install Guide](https://tailscale.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rsync, ssh, jq, SSH key authentication, and network access between configured peers.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
