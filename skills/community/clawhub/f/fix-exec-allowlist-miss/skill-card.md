## Description: <br>
Guides agents through diagnosing OpenClaw exec allowlist denials and applying hash-verified gateway configuration changes, including reload, restart, and Minimax cron auth troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rabbykst](https://clawhub.ai/user/rabbykst) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to investigate OpenClaw exec denials, adjust gateway tool profiles, and verify configuration changes while preserving hash-verified patch and rollback discipline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to broaden persistent gateway exec or profile settings, which may expand command execution access. <br>
Mitigation: Review the current gateway configuration with config.get first, require hash-verified patches, and keep the previous profile and security settings available for rollback. <br>
Risk: Patch examples or protected-path changes can cause unsafe or unintended gateway configuration changes. <br>
Mitigation: Use object-shaped config patches with the captured baseHash, avoid protected channel-specific paths, and verify the resulting profile and security settings after the patch. <br>
Risk: Troubleshooting Minimax cron authentication may involve sensitive OAuth or provider API credentials. <br>
Mitigation: Use system-level credential handling only where required, avoid exposing tokens in prompts or logs, and rotate or revoke credentials if they may have been shared. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline gateway commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include security-relevant configuration patch recommendations; users should verify current config and maintain a rollback path before applying changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
