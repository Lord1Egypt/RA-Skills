## Description: <br>
Check for new clawdbot releases and notify once per new version. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pors](https://clawhub.ai/user/pors) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Clawdbot users use this skill to check whether their local Clawdbot install is behind the latest GitHub release and to receive a one-time update notification. It can also configure a daily notification job when the user opts in. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A persistent daily check can notify the wrong recipient or channel if setup is run with incorrect delivery settings. <br>
Mitigation: Run setup only when scheduled notifications are wanted, verify the recipient and channel before enabling it, and uninstall with setup.sh --uninstall when no longer needed. <br>
Risk: The scripts use predictable temporary file paths, which can be unsafe on shared machines. <br>
Mitigation: Use the skill on trusted machines or update the scripts to use mktemp-style temporary files before deployment in shared environments. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pors/clawdbot-release-check) <br>
- [Clawdbot GitHub repository](https://github.com/clawdbot/clawdbot) <br>
- [Clawdbot GitHub releases](https://github.com/clawdbot/clawdbot/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown status and notification text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local state and cache files under ~/.clawdbot and can optionally add a daily notification job.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
