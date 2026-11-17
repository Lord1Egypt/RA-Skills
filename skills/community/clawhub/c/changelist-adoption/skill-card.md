## Description:

Sets up and maintains per-task changelist documentation in a repository, with one engineering record per verified code task, a two-level module index, adapted agent rules, and a verifier.

This skill is ready for commercial/non-commercial use.

## Publisher:

[falllee](https://clawhub.ai/user/falllee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering agents use this skill to adopt a repository-level changelist practice, write task-level engineering records after verified code changes, keep a searchable module index, and preserve the entry, index, code, and tests in the same commit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist repository-level agent rules that override an existing commit-only-when-asked policy and permit future auto-commits.

Mitigation: Adopt it only when persistent changelist rules are desired, and rewrite the rule block so existing commit-authorization policies keep precedence unless a human explicitly approves auto-commit behavior.

Risk: Installing with an unpinned latest package can fetch a different installer version than the one reviewed.

Mitigation: Use a pinned installer version or manually copy the reviewed skill artifact into the target repository.

Risk: The bundled verifier checks index link integrity but does not prove that changelist entries are accurate, complete, or based on real validation.

Mitigation: Require human review of generated entries and include exact verification commands and results before committing changelist documentation.

## Reference(s):

- [Skill definition](SKILL.md)
- [README](README.md)
- [Agent instruction rule template](references/agents-rules-template.md)
- [Changelist entry template](assets/entry-template.md)
- [Changelist index template](assets/index-template.md)
- [ClawHub skill listing](https://clawhub.ai/falllee/skills/changelist-adoption)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with file templates, repository rule text, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update changelist entries, an index README, agent instruction rules, and same-commit pathspec guidance in the target repository.]

## Skill Version(s):

1.0.2 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
