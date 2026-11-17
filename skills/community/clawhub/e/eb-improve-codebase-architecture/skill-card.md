## Description:

Explore a codebase to identify architectural refactoring opportunities that improve testability by deepening shallow modules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect a codebase for shallow, tightly coupled modules and design deeper module interfaces that are easier to test and maintain. It helps compare refactoring candidates, dependency strategies, test impact, and RFC-style issue content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may publish a GitHub issue before the user reviews the repository target and full issue content.

Mitigation: Change or override the workflow so it drafts the issue, displays the target repository and complete content, and requires explicit user approval before running the publish command.

Risk: Architecture recommendations may be incomplete or unsuitable if the exploration misses important coupling, ownership, or test constraints.

Mitigation: Review candidate modules, dependency categories, and proposed test changes before accepting a refactor plan.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emersonbraun/skills/eb-improve-codebase-architecture)
- [REFERENCE.md](artifact/REFERENCE.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with code sketches, comparison notes, RFC issue content, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a GitHub issue after the user selects an interface.]

## Skill Version(s):

1.0.0 (source: skill metadata and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
