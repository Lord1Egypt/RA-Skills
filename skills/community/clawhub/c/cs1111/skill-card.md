## Description: <br>
Collects local system, network, and filesystem diagnostics, runs shell commands for authorized security checks, and can produce JSON or Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qiqi704](https://clawhub.ai/user/qiqi704) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, security testers, and operators use this skill to collect authorized host diagnostics, inspect network and filesystem state, and summarize command results for troubleshooting or security review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill exposes an unrestricted local shell-command path through custom command execution. <br>
Mitigation: Install it only for authorized diagnostics, avoid custom commands unless fully trusted, and review each command before execution. <br>
Risk: Diagnostic reports may expose usernames, hostnames, network topology, directory listings, or raw command output. <br>
Mitigation: Review and redact generated JSON or Markdown reports before sharing them outside the authorized team. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qiqi704/cs1111) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [JSON or Markdown diagnostic reports with captured command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include hostnames, usernames, network details, directory listings, and command output; review and redact reports before sharing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
