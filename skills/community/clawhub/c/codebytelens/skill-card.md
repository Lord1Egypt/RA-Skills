## Description: <br>
CodeByteLens is a Python code intelligence toolbox that uses open-source search, AST analysis, and optional type-checking tools to inspect definitions, references, symbols, call structure, and complexity without an LSP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lxr-666](https://clawhub.ai/user/lxr-666) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code-review agents use this skill to inspect Python projects, find definitions and references, list symbols, summarize call structure, and produce lightweight complexity reports from local source files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Directory searches may scan more local files than intended when the user supplies a broad target path. <br>
Mitigation: Review the target path before running analysis and use the narrowest project or file path that covers the task. <br>
Risk: Optional local tooling and analyzer commands may be unavailable or fail in some environments. <br>
Mitigation: Install only the tools needed for the workflow and verify analyzer output on non-sensitive code before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lxr-666/codebytelens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and terminal text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads user-selected local Python files or directories; optional type-checking workflows may require installing pyright.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
