## Description:

AtomGit (GitCode) integration for agents that use curl and bash to review, approve, merge, and manage pull requests, repositories, issues, CI checks, and collaborators across Windows Git Bash, Linux, and macOS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to operate AtomGit repositories from shell workflows, including pull request review, approval, merge operations, repository inspection, issue management, CI status checks, and collaborator administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses persistent AtomGit tokens that may grant read or write access to repositories in the token scope.

Mitigation: Use a least-privilege token, keep it in environment or trusted configuration storage, and avoid passing tokens in command arguments or URLs.

Risk: Pull request approval, merge, batch, issue, and collaborator commands can modify AtomGit repositories.

Mitigation: Review the target owner, repository, pull request or issue number, and requested operation before running commands that approve, merge, update, or change collaborators.

Risk: The skill may read AtomGit credentials from OpenClaw configuration files outside the current workspace.

Mitigation: Confirm which configuration file is being used and remove or rotate credentials that should not be available to this skill.

Risk: The security evidence says the release overstates its safety controls despite matching its stated purpose.

Mitigation: Treat the ClawHub security verdict as authoritative, review the scripts before deployment, and monitor network operations performed with the configured token.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panchenbo/skills/atomgit-curl)
- [AtomGit API documentation](https://docs.atomgit.com/docs/apis/)
- [API-REFERENCE.md](artifact/API-REFERENCE.md)
- [commands.md](artifact/commands.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [shell commands, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, bash, network access to AtomGit, and an ATOMGIT_TOKEN with permissions scoped to the intended repositories.]

## Skill Version(s):

3.0.4 (source: frontmatter, release evidence, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
