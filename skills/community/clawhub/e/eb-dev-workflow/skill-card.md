## Description:

Master orchestrator for the full autonomous development lifecycle, coordinating feature intake, PRD creation, issue breakdown, architecture, QA planning, development, testing, code review, pull request management, and issue closure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emersonbraun](https://clawhub.ai/user/emersonbraun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate an end-to-end feature workflow from idea intake through PR merge and issue closure. It is intended for agent-assisted development sessions where structured planning, QA gates, implementation, testing, and review steps need to stay aligned.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be triggered broadly and then drive code, testing, GitHub issue, PR, and merge-related actions with limited per-step user control.

Mitigation: Require explicit confirmation before code changes, GitHub comments, issue closure, PR creation, and any merge-related action.

Risk: Users may activate an end-to-end autonomous development workflow when they only intended to plan or ask for next steps.

Mitigation: Install and use this skill only when the agent is expected to manage the full development workflow, and confirm the current phase before advancing.

## Reference(s):

- [Spec-Kit Reference Templates](artifact/references/spec-templates.md)
- [ClawHub Skill Page](https://clawhub.ai/emersonbraun/skills/eb-dev-workflow)
- [Publisher Profile](https://clawhub.ai/user/emersonbraun)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with workflow state blocks, checklists, issue comments, PR descriptions, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May coordinate code changes, test execution, GitHub issue comments, pull request creation, and issue closure through the hosting agent.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
