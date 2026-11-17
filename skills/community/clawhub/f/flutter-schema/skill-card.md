## Description:

Provides Flutter GetX three-layer architecture guidance for core, shared, and modules structure, plus page scaffold generation for new modules and code review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[symboy](https://clawhub.ai/user/symboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design, scaffold, and review Flutter applications that follow a GetX core, shared, and modules architecture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold generator can be tricked into writing new files outside the intended Flutter project folder through symlinks.

Mitigation: Run scripts/validate.py only in trusted Flutter repositories, avoid target directories containing symlinks, and review generated files before committing them.

## Reference(s):

- [Flutter GetX three-layer architecture schema](artifact/schema.md)
- [ClawHub skill page](https://clawhub.ai/symboy/skills/flutter-schema)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with optional generated Dart scaffold files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The page generator can write binding, logic, state, and view Dart files for a named GetX page.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
