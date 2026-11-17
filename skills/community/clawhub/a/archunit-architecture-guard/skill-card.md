## Description:

Scans Java/Kotlin projects to identify architecture patterns and smells, then generates ArchUnit guard tests and baseline guidance that help prevent new architecture violations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terryking1992](https://clawhub.ai/user/terryking1992)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Java/Kotlin project architecture, identify dependency and packaging problems, and generate ArchUnit tests that freeze existing violations while blocking new ones.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated ArchUnit rules and baseline files can change future test and CI behavior.

Mitigation: Review the generated rules, freeze configuration, and baseline store before committing them.

Risk: The skill reads the local Java/Kotlin source tree to build an architecture map.

Mitigation: Run it only in repositories intended for architecture review and avoid sharing reports that expose sensitive package or class names.

## Reference(s):

- [ArchUnit](https://github.com/TNG/ArchUnit)
- [ArchUnit cookbook](references/archunit-cookbook.md)
- [Architecture pattern detection reference](references/pattern-detection.md)
- [Architecture smell catalog](references/smell-catalog.md)
- [Package scanning helper](references/scan_packages.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Java/Kotlin code blocks, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write ArchUnit test files and archunit.properties into the user's repository when a project is available.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
