## Description:

Rétroaction et résolution des points bloquants pour l'automatisation Asana et Git dans KiloClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rez0](https://clawhub.ai/user/rez0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill as a troubleshooting reference for Asana-to-KiloClaw workflows, Git backup failures, token synchronization, state-file validation, repository hygiene, and cron scheduling conflicts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill text includes token-handling commands that can expose or persist GitHub and Asana secrets.

Mitigation: Use Git credential helpers, GitHub CLI, or a keychain-backed credential manager; retrieve Asana secrets at runtime from 1Password instead of storing plaintext token files.

Risk: Tokens may already have been stored in URLs or local token files if the documented commands were followed.

Mitigation: Rotate any affected GitHub or Asana tokens and remove plaintext credentials from remotes, files, shell history, and logs.

Risk: Cron and repository changes described by the skill can affect automation behavior.

Mitigation: Review scheduled jobs, Git remotes, .gitignore changes, and repository state before applying the guidance in an operational workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rez0/skills/asana-git-retex)
- [Publisher profile](https://clawhub.ai/user/rez0)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only troubleshooting guidance; no executable files are included in the artifact.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
