## Description:

Use when creating, migrating, or optimizing skills for this alicloud-skills repository. Use whenever users ask to add a new skill, import an external skill, refactor skill structure, improve trigger descriptions, add smoke tests under tests/**, or benchmark skill quality before merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cinience](https://clawhub.ai/user/cinience)

### License/Terms of Use:

Apache 2.0

## Use Case:

Developers and skill maintainers use this skill to create, migrate, refactor, validate, and benchmark skills in an alicloud-skills repository while following that repository's naming, layout, testing, and output conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local process termination may stop an unrelated service if the eval viewer is started on an occupied port.

Mitigation: Use a dedicated or confirmed-free port for the eval viewer, and review any port-kill action before running the tool in a shared workstation or CI environment.

Risk: Packaging imported or untrusted skill directories can disclose unintended files through symlinks or unexpected directory contents.

Mitigation: Package only trusted skill directories, inspect symlinks and included files first, and review the generated archive before distribution.

Risk: Description-improvement tooling may send skill and evaluation content to Anthropic.

Mitigation: Do not run that tooling on confidential, regulated, or proprietary skill/eval data unless third-party model processing is approved.

## Reference(s):

- [JSON Schemas](artifact/references/schemas.md)
- [Sources](artifact/references/sources.md)
- [Anthropic reference skill](https://github.com/anthropics/skills/tree/main/skills/skill-creator)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with code snippets, shell commands, configuration examples, and file-oriented implementation steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update skill files, smoke tests, validation outputs, benchmark JSON, and HTML review artifacts when used in a repository workspace.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
