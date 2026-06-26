## Description: <br>
Routes local coding requests across exploration, planning, implementation, debugging, refactoring, security review, safe command execution, and Git workflow skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sf0799](https://clawhub.ai/user/sf0799) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to decide which local coding workflow skill to invoke and in what order when a workspace task spans analysis, planning, implementation, validation, security review, or Git hygiene. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recommended downstream skills may write code, run commands, or manage Git, which can carry operational risk outside this routing skill. <br>
Mitigation: Review the selected downstream skill before invocation, especially for workflows that modify files, execute commands, or change repository history. <br>


## Reference(s): <br>
- [Routing Examples](references/routing-examples.md) <br>
- [ClawHub skill page](https://clawhub.ai/sf0799/code-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces selected skill names, invocation order, reasons for each selection, and the recommended stopping point for the current turn.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
