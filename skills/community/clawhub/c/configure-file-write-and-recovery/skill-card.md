## Description: <br>
Helps agents troubleshoot gateway configuration files that revert after restart and produce recovery guidance for durable configuration writes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[2070super](https://clawhub.ai/user/2070super) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when gateway configuration changes are lost after restart, especially when adding model IDs or recovering from automatic configuration restore behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may encourage persistent gateway configuration overwrites without enough safeguards. <br>
Mitigation: Use it only in a controlled gateway environment after confirming the exact config path and desired model IDs, backing up the existing file, validating the resulting config, and requiring explicit approval for any write or restart action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/2070super/configure-file-write-and-recovery) <br>
- [SKILL.md](SKILL.md) <br>
- [write_config.py](scripts/write_config.py) <br>
- [evals.json](evals/evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code and shell-command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose writing gateway configuration files and checking persistence after restart.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
