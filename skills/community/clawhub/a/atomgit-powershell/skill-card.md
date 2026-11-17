## Description:

AtomGit PowerShell helps agents work with the AtomGit/GitCode platform through PowerShell commands for authentication, pull request review, approval, merging, repository queries, issue management, batch processing, and CI status checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[panchenbo](https://clawhub.ai/user/panchenbo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to inspect and manage AtomGit repositories, pull requests, issues, collaborators, and CI status from PowerShell. It is especially relevant for review workflows that require authenticated PR comments, approvals, merges, or batch processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch PowerShell script can perform authenticated PR approvals when loaded or run with its default parameters.

Mitigation: Do not dot-source or run the batch script until it has been reviewed and changed so loading only defines functions; execute batch approvals only with explicit repository and PR arguments.

Risk: The skill can make live repository changes, including PR comments, approvals, merges, issue updates, and collaborator changes.

Mitigation: Use a least-privilege AtomGit token, confirm target owner, repository, and PR or issue numbers before execution, and review generated commands before running them.

Risk: Token exposure could allow unintended AtomGit API access.

Mitigation: Prefer environment-based token configuration, avoid tokens in command lines or URLs, and remove tokens from logs, shell history, and shared configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/panchenbo/skills/atomgit-powershell)
- [AtomGit API documentation](https://docs.atomgit.com/docs/apis/)
- [AtomGit token settings](https://atomgit.com/setting/token-classic)
- [README.md](README.md)
- [commands.md](commands.md)
- [API-REFERENCE.md](API-REFERENCE.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown with inline PowerShell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce authenticated AtomGit API actions when the generated or selected commands are executed with a valid token.]

## Skill Version(s):

3.0.1 (source: frontmatter, changelog, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
