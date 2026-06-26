## Description: <br>
Run a full spec-code audit on the Cathedral codebase after build waves, major refactors, or suspected spec-code drift; produce forward and reverse audits, a bug report, and a prioritized fix plan that can drive fixes through Claude Code sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hydroculator](https://clawhub.ai/user/hydroculator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to audit the Cathedral C# codebase for drift between specs and implementation, consolidate findings, prioritize remediation, and prepare scoped task briefings for follow-up code or spec changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can drive broad repository edits, shell commands, commits, and recurring monitoring. <br>
Mitigation: Run audit phases read-only where possible, review generated task briefings before launch, inspect diffs, and require human approval before commits. <br>
Risk: Recurring cron monitoring may continue beyond the intended audit session. <br>
Mitigation: Avoid the cron monitor unless needed, or tightly scope and remove it after the task completes. <br>
Risk: Parallel Claude Code sessions can exhaust memory on constrained hosts. <br>
Mitigation: Run audit batches sequentially on memory-constrained systems and verify `dotnet build` manually if a session is killed. <br>


## Reference(s): <br>
- [CC Task Briefing Template](references/cc-task-template.md) <br>
- [Cathedral Audit release page](https://clawhub.ai/hydroculator/cathedral-audit) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown reports, Markdown task briefings, shell commands, and repository change guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces audit reports, prioritized remediation plans, daily memory log entries, build verification steps, and commit guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
