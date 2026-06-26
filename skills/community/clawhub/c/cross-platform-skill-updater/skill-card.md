## Description: <br>
Checks and updates locally installed AI agent skills from git worktrees or .skill-lock.json lock files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viccwang](https://clawhub.ai/user/viccwang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams maintaining local agent skill installations use this skill to check status, identify safe updates, and update git or lock-file based skills across supported AI coding environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect and update local skill installations, including broad default search paths, which can change future agent behavior. <br>
Mitigation: Run check first, constrain scope with --path and --source, review repositories and lockfile sources before updating, and avoid broad global updates unless intended. <br>
Risk: Lock-file based updates can replace local skill folders. <br>
Mitigation: Use the built-in backup behavior, review reported sources and hashes, and confirm that local content has not drifted before applying updates. <br>


## Reference(s): <br>
- [Artifact README](README.md) <br>
- [ClawHub release page](https://clawhub.ai/viccwang/cross-platform-skill-updater) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports local skill status and can guide scoped updates for git and lock-file based installations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
