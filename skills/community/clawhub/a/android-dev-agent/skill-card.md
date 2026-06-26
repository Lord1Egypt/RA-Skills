## Description: <br>
Assist with AOSP builds, HAL analysis, Framework edits, ROM customization, and SDK/NDK issues using isolated environments and detailed reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[happysurfingeveryday-art](https://clawhub.ai/user/happysurfingeveryday-art) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Android platform developers and ROM engineers use this skill to investigate AOSP build failures, analyze HAL and Framework changes, customize ROM or kernel settings, and produce implementation guidance or patches. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Android source syncs, builds, and analysis commands can consume significant compute, storage, and time. <br>
Mitigation: Use a dedicated checkout or sandbox and review planned repo syncs and builds before execution. <br>
Risk: Framework, HAL, ROM, or kernel work can change local source files. <br>
Mitigation: Keep work in an isolated worktree and review generated patches before applying them to the primary workspace. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/happysurfingeveryday-art/android-dev-agent) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with command logs, analysis, patches, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports are named memory/reports/android-dev-{topic}-{date}.md when the workflow is followed.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
