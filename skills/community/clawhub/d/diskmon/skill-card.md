## Description: <br>
Watch disk space in real time and alert before storage runs low. Use when monitoring usage, finding large dirs, preventing disk-full events. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, system administrators, and operations teams use Diskmon to record, review, search, and export disk-related observations and maintenance notes from a local command-line logbook. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Diskmon records disk-related entries in local plaintext logs and export files. <br>
Mitigation: Do not enter secrets or sensitive infrastructure details unless storage under ~/.local/share/diskmon/ and generated export files are acceptable. <br>
Risk: Diskmon is a logbook and should not be treated as live monitoring, alerting, cleanup, backup, restore, or repair automation. <br>
Mitigation: Use it for recording and reviewing observations; rely on dedicated operational tools for automatic monitoring, alerting, remediation, backup, and restore workflows. <br>


## Reference(s): <br>
- [Diskmon ClawHub page](https://clawhub.ai/ckchzh/diskmon) <br>
- [ckchzh publisher profile](https://clawhub.ai/user/ckchzh) <br>
- [BytesAgain homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, configuration, guidance] <br>
**Output Format:** [Plain text command output with optional JSON, CSV, or TXT exports and inline shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local plaintext logs and exports under ~/.local/share/diskmon/.] <br>

## Skill Version(s): <br>
2.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
