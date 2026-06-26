## Description: <br>
Detect and fix TypeScript error handling anti-patterns with state persistence and approval workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Glucksberg](https://clawhub.ai/user/Glucksberg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to scan TypeScript projects for silent error handling failures, review proposed fixes, apply approved changes, and track cleanup progress across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run an external bunx antipattern-czar package against a repository. <br>
Mitigation: Install and run it only in repositories where that package execution is acceptable, and review command behavior before use. <br>
Risk: Review or auto mode can propose or apply source edits that change TypeScript error handling behavior. <br>
Mitigation: Use a clean git working tree, review all diffs, and run the project test suite before committing changes. <br>
Risk: .anti-pattern-state.json may contain file paths, history, or code snippets from the scanned repository. <br>
Mitigation: Do not share the state file when it contains sensitive content; delete it or add it to ignore rules when appropriate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Glucksberg/anti-pattern-czar) <br>
- [Anti-Pattern Patterns Reference](references/patterns.md) <br>
- [Workflow Details](references/workflows.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, TypeScript fix templates, and progress summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update .anti-pattern-state.json and propose repository edits during review or auto-fix workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
