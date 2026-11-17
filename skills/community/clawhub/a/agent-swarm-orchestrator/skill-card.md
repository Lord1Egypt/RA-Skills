## Description:

Orchestrate OpenClaw Agent Swarm workflows for multi-project coding automation with Obsidian task intake, Claude coding, Codex review, GitLab MR flow, merge+sync, and done-status closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[matzoh](https://clawhub.ai/user/matzoh)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to dispatch, monitor, review, publish, merge, and close coding tasks across local repositories. It is suited for operators who intentionally run a background coding automation control plane connected to Git provider CLIs, agent CLIs, Obsidian task notes, and notification targets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background agents can change code, create commits, push branches, open merge requests, and merge changes with weak safeguards.

Mitigation: Run under an isolated OS account with disposable worktrees, require explicit confirmation before pushes and merges, and review generated changes before accepting them.

Risk: The automation may run coding and review CLIs with dangerous sandbox or permission-bypass flags.

Mitigation: Remove dangerous bypass flags and use least-privilege agent, Git provider, and filesystem credentials before production use.

Risk: Obsidian task intake can trigger agent activity from local note content and shared folders.

Mitigation: Point the scanner only at trusted, private task folders and avoid shared or untrusted Obsidian vaults until interpolation issues noted by the security review are fixed.

Risk: Notification integrations and Git provider access can expose operational details or affect external services.

Mitigation: Use scoped tokens, private notification targets, and test notification delivery before unattended operation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/matzoh/skills/agent-swarm-orchestrator)
- [ClawHub publisher profile](https://clawhub.ai/user/matzoh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, JSON configuration examples, generated prompt text, logs, notifications, and merge-request descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces and updates local control-plane files such as task state, logs, prompt files, notification files, Git branches, worktrees, commits, and merge requests when installed and executed.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
