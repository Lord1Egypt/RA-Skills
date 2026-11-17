## Description:

Incremental backend API and frontend browser testing with persistent memory for monitoring commits, enriching insufficient commit messages, and running targeted tests scoped to changed files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tiansyao](https://clawhub.ai/user/tiansyao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Argus to bootstrap and maintain backend API and frontend browser regression tests from source routes, bug-fix history, and branch diffs. It records persistent test catalogs, runs targeted pytest and Playwright checks, and reports health scores and failing tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installs persistent Git automation and may amend commit messages before push.

Mitigation: Review .argus/commit-hook.sh and .git/hooks/post-commit after initialization, and avoid shared or signed-commit workflows unless hook and amendment behavior are explicitly approved.

Risk: Can install Python and Playwright dependencies during frontend test setup.

Mitigation: Run in a controlled development environment and review dependency installation before using the skill in an active repository.

Risk: Generated tests and reports can modify repository state under .argus and tests directories.

Mitigation: Inspect generated files before committing them and keep locked regression tests under human review.

## Reference(s):

- [ClawHub argus release page](https://clawhub.ai/tiansyao/skills/argus-qa)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown reports, generated Python test code, shell commands, and repository configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent .argus state, generated tests, reports, and a Git post-commit hook.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
