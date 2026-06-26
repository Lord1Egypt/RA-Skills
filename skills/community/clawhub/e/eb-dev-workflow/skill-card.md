## Description: <br>
Master orchestrator for the full autonomous development lifecycle, coordinating planning, issue breakdown, architecture, QA planning, development, testing, code review, and PR management for Claude Code workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emersonbraun](https://clawhub.ai/user/emersonbraun) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to coordinate an autonomous feature-development workflow from idea intake through PR merge. It is intended for repository work that benefits from explicit QA gates, delegated specialist skills, and structured GitHub issue and PR flow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can drive broad autonomous development and GitHub workflow actions from common planning or feature-development prompts. <br>
Mitigation: Use it only in trusted repositories and require explicit confirmation before code changes, test execution, GitHub comments, PR creation, merges, or issue closure. <br>
Risk: Delegated skills and GitHub credentials may expand the practical permissions available during the workflow. <br>
Mitigation: Verify delegated skills before use and keep GitHub credentials least-privilege for the intended repository tasks. <br>


## Reference(s): <br>
- [Dev Workflow ClawHub Page](https://clawhub.ai/emersonbraun/eb-dev-workflow) <br>
- [Spec-Kit Reference Templates](artifact/references/spec-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code blocks, checklists, shell commands, and structured status or report sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or coordinate repository changes, GitHub issue or PR text, test plans, test reports, and delegated skill instructions.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata; artifact frontmatter lists 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
