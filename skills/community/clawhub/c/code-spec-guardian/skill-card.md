## Description:

Code Spec Guardian analyzes project language, framework, architecture, API, SQL, Git, and style conventions, stores them in modular `.code-spec/` files, and applies them when an agent writes, reviews, refactors, or fixes code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gmmg55](https://clawhub.ai/user/gmmg55)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to analyze existing project conventions, generate modular `.code-spec/` guidance, and have agents apply those conventions during code generation, repair, refactoring, and review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update `AGENTS.md`, which can change how future agents behave in the repository.

Mitigation: Allow `AGENTS.md` edits only when persistent auto-loading is intended, and review the diff before keeping the change.

Risk: Architecture analysis can expose secret-bearing environment files if real `.env` files are read.

Mitigation: Use `.env.example` or names-only environment parsing, and avoid allowing the skill to read real `.env` values.

Risk: Generated `.code-spec/` files can steer future code generation and reviews with stale or incorrect project conventions.

Mitigation: Review generated specifications before relying on them, keep them under version control, and require confirmation for major convention changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gmmg55/skills/code-spec-guardian)
- [Code Spec Guardian README](artifact/README.md)
- [Code Spec Index](artifact/references/index.md)
- [Self-Evolution Mechanism](artifact/references/evolution.md)
- [Project Context Extractor](artifact/scripts/analyze_project.py)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, generated `.code-spec/` files, JSON project context, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update `.code-spec/` files and may update `AGENTS.md` after initial analysis when auto-loading guidance is desired.]

## Skill Version(s):

1.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
