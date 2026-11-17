## Description:

Operate the disinto autonomous code factory when managing factory agents, filing forge issues, reading agent journals, querying CI pipelines, checking the dependency graph, or inspecting factory health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johba37](https://clawhub.ai/user/johba37)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage a Disinto autonomous code factory, including agent health checks, issue creation, journal review, CI inspection, and dependency graph review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses credential-bearing API calls to forge and CI systems.

Mitigation: Install only in trusted repository environments, use least-privilege Forge and Woodpecker tokens, and verify API endpoints are trusted HTTPS URLs.

Risk: Local journal reads can expose repository-local operational state and have review-worthy path handling around the date argument.

Mitigation: Avoid allowing untrusted text to choose read-journal.sh arguments until date path handling is fixed, and keep PROJECT_REPO_ROOT scoped to the intended repository.

Risk: The server security verdict is suspicious because of scoping issues around journal reads and credential-bearing calls.

Mitigation: Review the configured environment, requested operation, and command output before deployment or repeated use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johba37/skills/disinto)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and command output summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local repository state and call configured Forgejo/Gitea or Woodpecker endpoints through user-provided environment variables.]

## Skill Version(s):

0.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
