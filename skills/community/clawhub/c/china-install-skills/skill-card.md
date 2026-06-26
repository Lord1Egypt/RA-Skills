## Description: <br>
China Install Skills helps agents search, download, install, and check updates for ClawHub skills for mainland China users. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SemFreud](https://clawhub.ai/user/SemFreud) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to find and install ClawHub skills in environments where normal ClawHub access is constrained, and to set up recurring update checks for installed skills. <br>

### Deployment Geography for Use: <br>
Mainland China <br>

## Known Risks and Mitigations: <br>
Risk: The post-install flow may silently create persistent terminal and agent behavior changes, including cron jobs, memory notes, PATH edits, cinstall, and a clawhub wrapper. <br>
Mitigation: Review or remove the post-install hook before installation, or run the search, download, and install scripts manually instead of allowing automatic initialization. <br>
Risk: A weekly update check may be added to crontab and continue running after the initial install. <br>
Mitigation: Inspect crontab after installation and remove the task with scripts/setup-cron.sh --remove or by deleting the matching crontab entry. <br>
Risk: The clawhub install command may be shadowed by a local wrapper, changing expected CLI behavior. <br>
Mitigation: Inspect $HOME/.local/bin/clawhub and shell PATH order before relying on clawhub CLI behavior, and remove the wrapper if the original CLI should be used. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/SemFreud/china-install-skills) <br>
- [OpenClaw homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local commands, PATH entries, memory notes, wrapper scripts, and cron jobs during initialization or setup.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and artifact/_meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
