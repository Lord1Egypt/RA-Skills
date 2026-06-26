## Description: <br>
Builds a persistent semantic index of Python source files so agents can find relevant classes, functions, and modules with natural-language queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryno2390](https://clawhub.ai/user/ryno2390) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and coding agents use this skill to build and query a local semantic index for Python projects, especially when they need to locate relevant symbols by meaning before editing or delegating code work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The persistent local index stores source-derived snippets, which may retain private code or secrets if sensitive files are indexed. <br>
Mitigation: Install only in repositories intended for indexing, exclude sensitive paths, and add `.codebase_index/` to `.gitignore`. <br>


## Reference(s): <br>
- [Integration Patterns](references/integration.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local semantic search guidance and code patterns; search calls return ranked symbol metadata and snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
