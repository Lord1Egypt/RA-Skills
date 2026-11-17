## Description:

Diagnoses structural maintainability problems in frontend code using concrete evidence, false-positive checks, and candidate refactorings without changing business code during diagnosis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bovinphang](https://clawhub.ai/user/bovinphang)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to identify frontend code smells, evaluate concrete evidence and false positives, and prioritize potential refactorings before making changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A proposed code smell or refactoring may be misleading without sufficient project context.

Mitigation: Check concrete file and symbol evidence, rule out false positives, and review suggested changes before applying them.

## Reference(s):

- [Code Smell Catalog](references/smell-catalog.md)
- [Code Smell Detection Guide](references/detection-guide.md)
- [Smell-to-Refactoring Map](references/smell-to-refactoring-map.md)
- [ClawHub release](https://clawhub.ai/bovinphang/skills/fec-code-smells)
- [Project repository listed in package metadata](https://github.com/bovinphang/frontend-craft)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown diagnostic findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings include location, evidence, smell ID, impact, confidence, priority, false-positive considerations, and candidate refactorings.]

## Skill Version(s):

2.9.0 (source: ClawHub release, package.json, metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
