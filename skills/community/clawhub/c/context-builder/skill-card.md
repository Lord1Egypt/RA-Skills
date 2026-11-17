## Description:

Generate LLM-optimized codebase context from any directory using context-builder CLI

This skill is ready for commercial/non-commercial use.

## Publisher:

[igorls](https://clawhub.ai/user/igorls)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to generate scoped, LLM-ready Markdown snapshots of codebases for review, onboarding, architecture analysis, diff updates, and API-surface inspection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The underlying CLI reads file contents from the specified directory, and generated context may include secrets or credentials embedded in source files.

Mitigation: Run only on explicit project directories, use scoped filters and ignore rules, and review generated context files before sharing.

Risk: Manual binary downloads create a supply-chain verification step for installers.

Mitigation: Prefer pinning the documented version, use locked installs when supported, and verify downloaded binaries against version-specific checksums.

## Reference(s):

- [Context Builder ClawHub Skill Page](https://clawhub.ai/igorls/skills/context-builder)
- [context-builder GitHub Repository](https://github.com/igorls/context-builder)
- [context-builder GitHub Releases](https://github.com/igorls/context-builder/releases/latest)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and TOML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can produce full codebase context, AST signatures, token-count previews, and diff-only updates depending on CLI flags.]

## Skill Version(s):

0.8.3-1 (source: server release metadata; artifact frontmatter reports 0.8.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
