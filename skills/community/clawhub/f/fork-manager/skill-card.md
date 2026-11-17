## Description:

Fork Manager helps agents sync forks, rebase pull-request branches, track PR state, and build production branches that combine open PRs with local patches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glucksberg](https://clawhub.ai/user/glucksberg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to keep personal forks current with upstream repositories, rebase active PR branches, preserve selected local patches, and summarize fork maintenance work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch, rebase, merge, push, and rewrite branches using Git and the user's GitHub CLI credentials.

Mitigation: Install it only for repositories where that authority is acceptable, review the target repo config before use, and rely on --force-with-lease rather than unsafe force pushes.

Risk: Persistent autoResolveConflicts can allow agents to automatically resolve and push conflict changes.

Mitigation: Leave autoResolveConflicts disabled unless automatic branch rewrites are acceptable, and review any semantic conflict resolutions before relying on them.

Risk: Configurable post-sync hooks can run repository-specific commands after upstream changes.

Mitigation: Use postSyncHooks only from trusted configs and inspect hook commands before enabling them.

Risk: Branch switching and production branch rebuilds can affect uncommitted work.

Mitigation: Check the working tree before destructive operations and stash uncommitted and untracked files as the artifact workflow describes.

## Reference(s):

- [Fork Manager on ClawHub](https://clawhub.ai/glucksberg/skills/fork-manager)
- [Publisher profile](https://clawhub.ai/user/glucksberg)
- [README](artifact/README.md)
- [Architecture](artifact/ARCHITECTURE.md)
- [OpenClaw Skills Docs](https://github.com/openclaw/openclaw/blob/main/docs/tools/skills.md)
- [ClawHub](https://clawhub.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline shell commands and JSON configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update per-repository config and history files while reporting actions, conflicts, and review items.]

## Skill Version(s):

2.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
