## Description:

A generic test writing discipline that promotes test quality, real assertions, and resistance to anti-patterns when writing or fixing tests across languages and frameworks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iliaal](https://clawhub.ai/user/iliaal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill when writing tests, adding coverage, or fixing failing tests. It guides them to create discriminating behavioral tests that assert user-visible outcomes and catch regressions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cleanup guidance includes database or volume deletion steps that could remove persistent data.

Mitigation: Review cleanup instructions and verify targets are disposable test resources with important data backed up before deleting databases or volumes.

Risk: The documentation describes an evaluation tool whose implementation was not supplied, so its behavior remains uncertain.

Mitigation: Review the evaluation tool implementation or treat its behavior as unverified before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iliaal/skills/compound-eng-writing-tests)
- [anti-patterns-extended.md](references/anti-patterns-extended.md)
- [false-pass-oracle-traps.md](references/false-pass-oracle-traps.md)
- [generated-corpus-techniques.md](references/generated-corpus-techniques.md)
- [isolation-and-sandbox-traps.md](references/isolation-and-sandbox-traps.md)
- [oracle-smells.md](references/oracle-smells.md)
- [rationalization-table.md](references/rationalization-table.md)
- [regression-proof.md](references/regression-proof.md)
- [test-completion.md](references/test-completion.md)
- [test-design.md](references/test-design.md)
- [test-smells.md](references/test-smells.md)

## Skill Output:

**Output Type(s):** [Code, Guidance, Shell commands]

**Output Format:** [Test code and concise guidance in the repository's existing language and framework formats, with relevant shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Follows the repository's test runner, configuration, and conventions]

## Skill Version(s):

5.1.7 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
