## Description:

Provides Git engineering guidance for branching strategy, commit standards, code review, release automation, monorepo management, repository security, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1kalin](https://clawhub.ai/user/1kalin)

### License/Terms of Use:


## Use Case:

Developers and engineering teams use this skill to assess repository health, choose Git workflows, and generate practical branch protection, pull request, CODEOWNERS, CI, release, security, and recovery guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some generated Git guidance may include history rewrite, reset, force-push, hook, or global Git configuration commands that can affect repository state or developer environments.

Mitigation: Review commands before execution, prefer repository-local settings, test destructive recovery steps on a disposable clone or branch, and keep branch protection enabled for shared branches.

Risk: Some examples use npx-style commands that can download tooling dynamically.

Mitigation: Prefer pinned local development dependencies or checked-in package scripts before running generated tool commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1kalin/skills/afrexai-git-engineering)
- [AfrexAI Context Packs](https://afrexai-cto.github.io/context-packs/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, YAML snippets, shell commands, checklists, and decision tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include repository health scores, branching recommendations, pull request templates, CODEOWNERS rules, CI and release snippets, and recovery playbooks.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
