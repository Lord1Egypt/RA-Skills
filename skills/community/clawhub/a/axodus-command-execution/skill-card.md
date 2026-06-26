## Description: <br>
Execute terminal commands safely with preflight checks and risk gating. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mzfshark](https://clawhub.ai/user/mzfshark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run tests, builds, linters, migrations, and repository inspection commands with preflight risk checks and auditable command results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Terminal commands can modify files, affect global state, or perform destructive, installer, network, or remote-script actions. <br>
Mitigation: Review each command, working directory, expected side effects, and high-risk action before allowing execution; prefer dry-run or scoped commands when available. <br>
Risk: The RedHat-style publisher naming is not verified by server evidence. <br>
Mitigation: Treat the publisher as the server-resolved ClawHub user mzfshark and rely on independent trust in that publisher before installation. <br>
Risk: The security summary notes malformed activation metadata. <br>
Mitigation: Review and fix activation metadata before depending on automatic invocation behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mzfshark/axodus-command-execution) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text, guidance] <br>
**Output Format:** [YAML-style structured text with command result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes command, purpose, result, exit code, key output lines, and next steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
