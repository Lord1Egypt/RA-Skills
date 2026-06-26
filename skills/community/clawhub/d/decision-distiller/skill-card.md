## Description: <br>
Distill decision contexts, options, trade-offs, and outcomes into structured decision records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, and developers use this skill to document decisions, compare options, capture rationale and trade-offs, and review past decision records for patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can create local Markdown files containing decision details in the default data folder or in a directory set by DECISION_DATA_DIR. <br>
Mitigation: Review the storage location before use and avoid recording sensitive personal or business decisions in an untrusted or shared directory. <br>
Risk: Decision records, summaries, and pattern analyses can preserve incomplete assumptions or misleading rationale if the input conversation is incomplete. <br>
Mitigation: Review generated records before relying on them and update outcomes and lessons as new information becomes available. <br>


## Reference(s): <br>
- [Decision Templates](references/decision-templates.md) <br>
- [Decision Analysis Frameworks](references/analysis-frameworks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown decision records, summaries, pattern analyses, status reports, and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local Markdown decision files in the default skill data folder or in DECISION_DATA_DIR when helper scripts are used.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
