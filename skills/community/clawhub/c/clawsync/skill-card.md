## Description: <br>
Backup and restore your OpenClaw workspace to GitHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickconstantinou](https://clawhub.ai/user/nickconstantinou) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use Clawsync to back up selected OpenClaw workspace identity, skill, and script files to a GitHub repository and restore them when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and mutate selected workspace files, restore files from GitHub, and potentially push changes. <br>
Mitigation: Review the scripts and agent instructions before use, back up the current workspace before restore, and require explicit confirmation before commit, push, deletion, or restore operations. <br>
Risk: Credential handling may persist GitHub credentials when token-based fallback authentication is used. <br>
Mitigation: Prefer gh-based or temporary authentication and avoid long-lived persistent git credential storage. <br>


## Reference(s): <br>
- [Clawsync on ClawHub](https://clawhub.ai/nickconstantinou/clawsync) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and environment-variable settings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires GITHUB_TOKEN, BACKUP_REPO, and OPENCLAW_WORKSPACE environment variables.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
