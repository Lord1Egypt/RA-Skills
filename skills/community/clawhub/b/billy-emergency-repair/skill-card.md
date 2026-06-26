## Description: <br>
Guides an authorized operator through emergency Billy authentication repair by backing up configuration, clearing stale tokens, restarting the gateway, and reporting results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Highlander89](https://clawhub.ai/user/Highlander89) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Neill or the authorized Billy administrator uses this skill during authentication or gateway emergencies to run the documented repair flow, preserve configuration backups, and collect logs for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can delete authentication tokens and restart the Billy gateway on a remote system. <br>
Mitigation: Run it only after explicit authorization from Neill or the authorized Billy administrator, and confirm current backups and rollback access before making changes. <br>
Risk: The repair flow depends on local scripts and persistent SSH access that were not included for review in the artifact. <br>
Mitigation: Inspect the referenced scripts locally, verify the SSH key is restricted and revocable, and confirm Tailscale connectivity before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Highlander89/billy-emergency-repair) <br>
- [Skill source documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance, Markdown] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes authorization checks, troubleshooting steps, expected log locations, and manual verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
