## Description:

Manage GitHub repositories, pull requests, issues, and workflows from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and repository maintainers use this skill to review pull requests, triage issues, inspect GitHub Actions state, and coordinate repository operations from OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can support high-impact repository actions when used with a GitHub credential.

Mitigation: Use a narrowly scoped token for the intended repositories and verify the target repository before write actions.

Risk: Repository write operations such as merges, branch deletion, releases, issue closure, or multi-repo changes can have broad project impact.

Mitigation: Require explicit confirmation before merges, branch deletion, releases, issue closure, or multi-repo changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-github-manager)
- [GitHub token settings](https://github.com/settings/tokens)
- [GitHub REST API endpoint](https://api.github.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented text with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a GITHUB_TOKEN with repository scopes appropriate to the requested GitHub action.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
