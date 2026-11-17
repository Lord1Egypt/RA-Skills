## Description:

This prompt-only skill helps agents analyze frontend project architecture, evaluate technology choices, review component design, assess build configuration, inspect monorepo and VSCode extension structure, and produce structured improvement guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wscats](https://clawhub.ai/user/wscats)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and frontend teams use this skill to review Vue, React, Angular, OpenHarmony, VSCode Extension, and monorepo projects. It produces architecture health assessments with scores, strengths, weaknesses, and prioritized refactoring suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate on broad frontend architecture terms and produce project review guidance when the user's intent is ambiguous.

Mitigation: Confirm the requested review scope before performing a full architecture assessment.

Risk: Architecture review may require project structure, package metadata, configuration files, or code snippets that could contain sensitive implementation details.

Mitigation: Ask users to share only files they are comfortable having analyzed and to redact secrets or proprietary details before review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wscats/skills/eno)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [frontend-arch-skill.md](artifact/frontend-arch-skill.md)
- [Jest Architecture](https://github.com/Wscats/jest-tutorial)
- [Dependency Injection Framework](https://github.com/Wscats/dependency-injection)
- [Lerna Tutorial](https://github.com/Wscats/lerna-tutorial)
- [GitHub Actions Tutorial](https://github.com/Wscats/github-actions-tutorial)
- [OpenHarmony Sheet](https://github.com/Wscats/sheet)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown architecture review reports with scoring tables, findings, and prioritized recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only output; no tool calls, API calls, or executable artifacts are produced by the skill itself.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
