## Description: <br>
Analyzes authorized workplace traces from tools such as DingTalk/Wukong dws or Google Workspace to identify repetitive work friction and produce automation SOP opportunities, Skill requirement cards, daily report drafts, and tomorrow's tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nopedijah](https://clawhub.ai/user/nopedijah) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and workflow automation builders use this skill to review authorized work activity, find repeatable friction, and turn the findings into evidence-backed automation opportunities, SOP or Skill requirement cards, report drafts, and follow-up tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may access workplace productivity data through authorized connectors. <br>
Mitigation: Review connector permissions before use and keep access limited to authorized work sources. <br>
Risk: Generated write actions, task creation, table updates, or message drafts could affect workplace records or communications. <br>
Mitigation: Require explicit user confirmation before any write, task-creation, table-update, or message-sending action runs. <br>
Risk: Work traces may include customer, contract, finance, HR, or other sensitive content. <br>
Mitigation: Summarize sensitive content instead of exposing raw details, and confirm any sharing or persistence step with the user. <br>


## Reference(s): <br>
- [dws product command summary](artifact/references/dws-products.md) <br>
- [Ecosystem adapter notes](artifact/references/ecosystem-adapters.md) <br>
- [Friction identification workflow](artifact/references/workflow.md) <br>
- [Output template](artifact/references/output-template.md) <br>
- [ClawHub skill release page](https://clawhub.ai/nopedijah/efficiency-gold-miner-sop-alchemy-universal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with structured tables, checklists, evidence summaries, and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include evidence sources and closed-loop status; write, task-creation, table-update, and message-sending actions require user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
