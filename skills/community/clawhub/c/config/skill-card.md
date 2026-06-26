## Description: <br>
Manage app configuration files with init, list, and add operations. Use when initializing configs, listing settings, switching environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bytesagain1](https://clawhub.ai/user/bytesagain1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to initialize local configuration notes, log configuration changes, search saved entries, and export stored records from a shell workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configuration notes and command arguments can persist sensitive text in plaintext local logs. <br>
Mitigation: Use the skill only for non-secret notes; do not store tokens or credentials in entries or command arguments, and inspect local logs if sensitive text may have been recorded. <br>
Risk: The documented remove command does not reliably delete stored entries. <br>
Mitigation: Do not rely on remove for deletion until the script is fixed; manually inspect and edit data.log and history.log when removal is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/bytesagain1/config) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text command output and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally and writes configuration notes and command history to local log files.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
