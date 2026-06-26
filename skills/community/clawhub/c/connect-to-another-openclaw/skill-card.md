## Description: <br>
Connect to and manage another OpenClaw server remotely via SSH, including health checks, skill synchronization, gateway restarts, and channel monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangbb-coder](https://clawhub.ai/user/fangbb-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to administer a trusted remote OpenClaw server, inspect gateway and channel status, resolve common port conflicts, compare installed skills, and synchronize skills between local and remote environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use SSH credentials to administer a remote OpenClaw server. <br>
Mitigation: Use it only with a trusted host, a dedicated least-privilege SSH key, and a non-root account where possible. <br>
Risk: The fix-port action can kill matching processes and restart the remote gateway. <br>
Mitigation: Run diagnostic actions first and use fix-port only during an acceptable maintenance window. <br>
Risk: Skill synchronization can install skills locally or remotely, especially when --yes bypasses prompts. <br>
Mitigation: Avoid --yes by default and review each skill before syncing from or to another host. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fangbb-coder/connect-to-another-openclaw) <br>
- [Publisher profile](https://clawhub.ai/user/fangbb-coder) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text and Markdown-style command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote command output, status summaries, skill comparison results, and installation or troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
