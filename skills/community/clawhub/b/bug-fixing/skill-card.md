## Description: <br>
Zero-regression bug fix workflow for triage, reproduction, root cause analysis, impact analysis, fixes, verification, knowledge deposit, and self-reflection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TinkCarlos](https://clawhub.ai/user/TinkCarlos) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to investigate and fix software bugs with evidence-driven reproduction, root cause confirmation, scoped changes, regression verification, and post-fix learning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may edit project files and produce code changes while fixing bugs. <br>
Mitigation: Keep the project under version control, review diffs before accepting changes, and run the prescribed tests and regression checks. <br>
Risk: The skill may run local verification commands, restart backend services, or clear Python cache files. <br>
Mitigation: Confirm the target project path and service process before allowing restarts, cache deletion, or process-kill commands. <br>
Risk: Persistent bug records could capture sensitive project details if the user includes them in bug evidence. <br>
Mitigation: Do not place secrets, credentials, or private customer data in bug records, logs, or reproduction notes. <br>


## Reference(s): <br>
- [Backend Common Issues & Fix Patterns](references/backend-patterns.md) <br>
- [AI Blind Spot Registry](references/blind-spots.md) <br>
- [Bug Pattern Library](references/bug-patterns.md) <br>
- [Bug Records - Project-Specific Bug Documentation](references/bug-records.md) <br>
- [Frontend Common Issues & Fix Patterns](references/frontend-patterns.md) <br>
- [Zero-Regression Verification Matrix](references/regression-matrix.md) <br>
- [System-Level Root Cause Analysis](references/system-rca.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with code snippets, command suggestions, bug summaries, verification reports, code review notes, and self-reflection scoring.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update project-local bug records and pattern references as part of the bug-fixing workflow.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
