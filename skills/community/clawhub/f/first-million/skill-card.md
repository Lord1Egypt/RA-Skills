## Description: <br>
Personal finance companion for tracking income, expenses, budgets, and progress toward a first-million savings goal using local scripts and reference guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuiguopengs](https://clawhub.ai/user/cuiguopengs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to record personal income and expenses, set and check budgets, generate spending summaries, and estimate progress toward a long-term savings target. It is most useful when the agent is expected to run the bundled local finance scripts and summarize the resulting reports in concise user-facing prose. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores sensitive income, expense, note, ledger, and budget history persistently in ~/.openclaw/workspace/first-million/. <br>
Mitigation: Install only if persistent local finance records are acceptable, use explicit wording before logging or changing records, and inspect or remove ledger.json and budget.json when the data should no longer be retained. <br>
Risk: Security evidence notes inconsistent project-local scope wording for the persistent finance data location. <br>
Mitigation: Treat ~/.openclaw/workspace/first-million/ as the effective data scope and review the generated ledger and budget files before relying on or sharing the records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cuiguopengs/first-million) <br>
- [Budgeting guide](references/budget-guide.md) <br>
- [Finance tips](references/finance-tips.md) <br>
- [Category guide](references/categories.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or plain text with optional local Python script commands and finance summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local JSON ledger and budget files in ~/.openclaw/workspace/first-million/ when the user asks to log transactions or set budgets.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
