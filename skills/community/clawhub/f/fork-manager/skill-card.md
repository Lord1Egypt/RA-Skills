## Description: <br>
Manage forks with open PRs by syncing upstream, rebasing branches, tracking PR status, and maintaining production branches with pending contributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[glucksberg](https://clawhub.ai/user/glucksberg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to keep forks current with upstream repositories, rebase PR branches, rebuild a production branch from open PRs and local patches, and review closed or obsolete PR work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide authenticated GitHub operations that affect PR review workflows and repository branches. <br>
Mitigation: Use it only when intentionally delegating fork or PR maintenance, and review generated comments, labels, close actions, proof-publish actions, pushes, and force-with-lease updates before execution. <br>
Risk: Automatic conflict resolution can change PR branch content and may mis-handle semantic conflicts. <br>
Mitigation: Enable automatic resolution only when appropriate, review conflict classifications, and manually inspect branches marked for semantic review before relying on the rebuilt production branch. <br>
Risk: Production-branch rebuilds and branch deletion steps can affect local work if a repository has uncommitted changes. <br>
Mitigation: Follow the documented preflight check and stash untracked, unstaged, and staged files before destructive branch operations, then restore the stash after completion. <br>


## Reference(s): <br>
- [Fork Manager README](README.md) <br>
- [Fork Manager Architecture](ARCHITECTURE.md) <br>
- [OpenClaw Skills Docs](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/glucksberg/fork-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with inline shell commands and JSON configuration updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append execution history per managed repository and update local JSON config files when the user runs the documented workflows.] <br>

## Skill Version(s): <br>
2.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
