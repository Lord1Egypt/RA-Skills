## Description: <br>
Scans Java/Kotlin projects to identify architecture patterns and smells, then provides refactoring guidance and ArchUnit guard tests that freeze existing violations while blocking new architecture drift. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terryking1992](https://clawhub.ai/user/terryking1992) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to analyze JVM project structure, detect architecture erosion, and add ArchUnit tests that preserve intended boundaries while allowing existing violations to be frozen as a baseline. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate or modify architecture tests and recommendations across a repository, and its trigger wording may be broader than ideal. <br>
Mitigation: Invoke it with a clear target path, review proposed findings and generated tests before committing them, and confirm before allowing repository-wide changes. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/terryking1992/archunit-architecture-guard) <br>
- [ArchUnit](https://github.com/TNG/ArchUnit) <br>
- [ArchUnit Cookbook](references/archunit-cookbook.md) <br>
- [Pattern Detection](references/pattern-detection.md) <br>
- [Architecture Smell Catalog](references/smell-catalog.md) <br>
- [Package Scanner](references/scan_packages.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown report with Java/Kotlin-oriented code blocks, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create ArchUnit test files and archunit.properties when operating on a local project; defaults to frozen baselines for existing violations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
