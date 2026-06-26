## Description: <br>
Data Sync helps agents synchronize Claude Code configuration, skills, hooks, memory, and related work repositories across machines through a relay server, with GitHub used for milestone archives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mwangxiang](https://clawhub.ai/user/mwangxiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and Claude Code users use this skill to coordinate initialization, pull, push, backup, and status workflows for Claude configuration and knowledge repositories across multiple computers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move Claude configuration and memory through a hardcoded root SSH server and GitHub account. <br>
Mitigation: Change the server, paths, and repositories to destinations you control, and prefer a restricted git-only SSH user instead of root. <br>
Risk: The artifact documents unsafe token handling patterns for GitHub credentials. <br>
Mitigation: Avoid PATs in URLs or shell commands; use deploy keys or a credential manager with least-privilege access. <br>
Risk: Syncing Claude skills, hooks, settings, or memory can propagate sensitive or unintended local state. <br>
Mitigation: Inspect diffs before syncing and scan changes before installing or pushing them. <br>


## Reference(s): <br>
- [sync-registry.md](sync-registry.md) <br>
- [ClawHub Data Sync listing](https://clawhub.ai/mwangxiang/data-sync) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and git/SSH command sequences] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces init, pull, push, backup, and status reports; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
