## Description:

Intelligent codebase analysis and understanding with caching. Automatically explores project structure, identifies modules, analyzes dependencies, and answers questions about the codebase. Use when onboarding to a new project, before refactoring, or when you need to understand code relationships.

This skill is ready for commercial/non-commercial use.

## Publisher:

[michealxie001](https://clawhub.ai/user/michealxie001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect unfamiliar or changing codebases, locate symbols, understand dependencies, ask code-structure questions, and generate architecture diagrams before onboarding, refactoring, or review work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically loads a project-local pickle cache, which can execute code if the cache is supplied by an untrusted repository.

Mitigation: Use the skill only on trusted repositories unless the pickle cache behavior is fixed; delete or ignore existing .codebase-intelligence/codebase_index.pkl files before running.

Risk: Local cache and export files may include source-code snippets or repository structure from the analyzed project.

Mitigation: Prefer a private trusted cache directory outside the repository and review generated cache, JSON, Markdown, and diagram outputs before sharing.

## Reference(s):

- [Codebase Intelligence Skill Page](https://clawhub.ai/michealxie001/skills/codebase-intelligence)
- [michealxie001 Publisher Profile](https://clawhub.ai/user/michealxie001)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, JSON exports, Mermaid or DOT diagrams, and command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local cache and export files that include codebase metadata and source snippets.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
