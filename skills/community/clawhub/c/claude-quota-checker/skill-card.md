## Description: <br>
Checks remaining Claude Max or Claude Pro subscription quota by running Claude Code CLI's /usage command through tmux and reporting plan, usage, and reset timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mfang0126](https://clawhub.ai/user/mfang0126) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to check remaining subscription quota, diagnose possible rate-limit issues, and see when usage windows reset. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The script launches the local Claude Code CLI through tmux and uses the current Claude login. <br>
Mitigation: Run it only with trusted tmux, git, and Claude Code binaries, and review the script before execution. <br>
Risk: The script auto-trusts a temporary scratch folder to read quota details. <br>
Mitigation: Confirm this behavior is acceptable for the local environment before running the quota check. <br>
Risk: Quota parsing depends on the Claude Code CLI /usage output format. <br>
Mitigation: Treat unexpected or empty results as a signal to re-run Claude Code manually and verify the usage screen. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mfang0126/claude-quota-checker) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown instructions and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local tmux, git, Claude Code CLI, and an active Claude Code login.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
