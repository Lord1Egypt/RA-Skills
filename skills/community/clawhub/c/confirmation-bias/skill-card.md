## Description: <br>
Guides an agent to challenge one-sided evidence by stating the claim, constructing falsification tests, auditing evidence-seeking, reassessing ambiguous evidence, and installing structural countermeasures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[deciqai](https://clawhub.ai/user/deciqai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external users, and developers use this skill to test claims or decisions that may be advancing on only supporting evidence. It helps agents identify falsification criteria, seek counter-evidence, and set update conditions before a team commits. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may treat the debiasing checklist as a substitute for domain review on material decisions. <br>
Mitigation: Use the skill as decision support and assign an accountable reviewer, devil's advocate, or red-team owner before acting on important conclusions. <br>
Risk: The skill may be applied where one-sided argument is intentional or the stakes are too low for structured disconfirmation. <br>
Mitigation: Apply the skill's stated exclusions for advocacy contexts, low-stakes decisions, and cases where the cost of disconfirmation exceeds the decision value. <br>


## Reference(s): <br>
- [ClawHub Skill Listing](https://clawhub.ai/deciqai/skills/confirmation-bias) <br>
- [Sources - confirmation-bias](references/sources.md) <br>
- [Peter Wason's 2-4-6 Task, 1960](examples/peter-wasons-2-4-6-task-1960.md) <br>
- [deciqAI](https://deciqai.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown checklist and structured analysis template] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May pause for user input in coach mode before advancing to later steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
