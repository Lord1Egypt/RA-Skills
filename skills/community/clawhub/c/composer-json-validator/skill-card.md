## Description:

Validate and lint PHP Composer composer.json files for structure, dependencies, autoload, and best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect PHP Composer composer.json files for structural issues, dependency hygiene, autoload configuration, lifecycle-script concerns, and project configuration best practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Composer lifecycle scripts can execute arbitrary commands during install or update.

Mitigation: Use this skill as a convenience linter and manually review lifecycle scripts before running composer install or composer update, especially commands invoking shells, interpreters, URLs, or downloaded content.

Risk: The validator is not a complete Composer security audit.

Mitigation: Treat clean output as a starting point and supplement it with project-specific dependency, script, and package-source review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/composer-json-validator)
- [Publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, guidance]

**Output Format:** [Plain text, JSON, or Markdown reports with issue summaries and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports lint, dependencies, scripts, and validate commands; strict mode can fail on warnings for CI use.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
