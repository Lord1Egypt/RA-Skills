## Description:

Complete Claude Code productivity system: project setup, prompting patterns, sub-agent orchestration, context management, debugging, refactoring, TDD, and shipping faster without scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill as a Claude Code workflow guide for project setup, prompting, context management, debugging, refactoring, test-driven development, git workflows, reviews, and production readiness checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad natural-language workflow guidance may lead an agent to propose project setup, git, or refactoring actions that are not appropriate for a specific codebase.

Mitigation: Invoke the skill deliberately and review generated CLAUDE.md, .claueignore, git, and refactoring actions before applying them to a real project.

Risk: The skill provides process guidance rather than executable safeguards, so generated code or commands still require project-specific validation.

Mitigation: Use the included review, testing, linting, type-checking, and production checklist practices before accepting or deploying generated changes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/1kalin/skills/afrexai-claude-code-production)
- [README](artifact/README.md)
- [Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, checklists, workflow templates, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only guidance; no executable code is shipped in the release artifact.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
