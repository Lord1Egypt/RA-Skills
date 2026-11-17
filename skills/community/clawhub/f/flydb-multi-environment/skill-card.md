## Description:

Organizes Flydb multi-database, multi-environment migration releases with configuration matrices, external password injection, JSON/Plan approval gates, baselines for existing databases, and offline driver handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zzxcoding](https://clawhub.ai/user/zzxcoding)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and release engineers use this skill to plan and automate Flydb database migrations across multiple database families and deployment environments. It helps structure versioned configuration, CI approval gates, baseline onboarding, and offline driver distribution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated CI workflows may execute changes against production databases.

Mitigation: Review all generated CI scripts, require a real approval gate before migrate, and bind approval to the target, configuration, and migration artifacts.

Risk: Database credentials may be exposed if placed in versioned files, command-line arguments, shell history, or CI logs.

Mitigation: Keep passwords in a secret manager or protected password file, inject them through environment variables or files, and avoid command-line password flags.

Risk: Automated repair, undo, clean, retry, or background execution can hide destructive or unknown migration outcomes.

Mitigation: Run migrations in the foreground with captured exit codes, verify the database state before retrying unknown outcomes, and keep repair, undo, and clean as manual actions.

## Reference(s):

- [Multi-environment automation reference](artifact/references/multi-environment.md)
- [Flydb GitHub project](https://github.com/zzxCoding/Flydb)
- [Flydb Gitee mirror](https://gitee.com/zzhenxuan/Flydb)
- [ClawHub skill page](https://clawhub.ai/zzxcoding/skills/flydb-multi-environment)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to Flydb CLI 0.3.x multi-environment migration workflows and should be reviewed before production database changes.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
