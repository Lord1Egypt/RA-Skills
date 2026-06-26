## Description: <br>
Backup OpenClaw configuration file with hash-based change detection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to back up an OpenClaw JSON configuration file, validate it as JSON5, and skip duplicate backups when the file content has not changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates additional local copies of configuration data. <br>
Mitigation: Use it only for the intended OpenClaw configuration file and choose a private backup directory. <br>
Risk: The helper depends on the json5 Python package. <br>
Mitigation: Install json5 only from a trusted package source if it is missing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/claw-config-backup) <br>
- [Publisher profile](https://clawhub.ai/user/goog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Files] <br>
**Output Format:** [Markdown with inline shell commands and local backup files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces timestamped local backup copies and status messages; skips backup when the latest matching backup has the same SHA256 hash.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
