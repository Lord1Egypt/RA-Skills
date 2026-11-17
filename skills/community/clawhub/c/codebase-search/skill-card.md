## Description:

Builds a persistent ChromaDB semantic index over Python source files so agents can find relevant classes, functions, or modules with natural-language queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryno2390](https://clawhub.ai/user/ryno2390)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to build and query a local semantic index for Python codebases, especially before implementing changes or delegating work to another agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing repositories that contain secrets or sensitive Python source can persist searchable snippets in a local .codebase_index/ directory.

Mitigation: Run the skill only against repositories approved for local indexing, avoid broad home-directory targets, and exclude or remove secret-bearing files before building the index.

Risk: The generated index is a local artifact that may be accidentally committed or shared.

Mitigation: Add .codebase_index/ to .gitignore before use and keep the persistence directory out of source control and release packages.

Risk: Installing an unpinned chromadb dependency can change behavior across environments.

Mitigation: Use a virtual environment and pin chromadb and its transitive dependencies for repeatable deployments.

## Reference(s):

- [Integration Patterns for Codebase Search](references/integration.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets; search results contain file paths, symbols, line numbers, docstrings, snippets, and relevance scores.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and reuses a local .codebase_index/ ChromaDB persistence directory under the target repository unless a custom persist_dir is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
