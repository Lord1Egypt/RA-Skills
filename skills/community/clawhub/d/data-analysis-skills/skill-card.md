## Description: <br>
Analyzes structured data such as tables, CSV, and Excel content to identify objects, attributes, relationships, risks, and action-oriented findings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renshengruozhiruchujian-sudo](https://clawhub.ai/user/renshengruozhiruchujian-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and data analysts use this skill to inspect structured datasets, connect related tables, validate findings with deterministic calculations, and produce decision-oriented analysis reports with sensitivity notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can ask an agent to reason over private HR, salary, customer, financial, or compliance data. <br>
Mitigation: Ask the agent to redact identifiers, summarize reasoning, and avoid reproducing raw rows unless necessary. <br>
Risk: Detailed reasoning-style output may expose sensitive intermediate data or derived sensitive conclusions. <br>
Mitigation: Limit outputs to the minimum fields needed for the decision and keep sensitive conclusions restricted to appropriate reviewers. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/renshengruozhiruchujian-sudo/skills/data-analysis-skills) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [REFERENCE.md](artifact/REFERENCE.md) <br>
- [ROLES.md](artifact/ROLES.md) <br>
- [EXAMPLES.md](artifact/EXAMPLES.md) <br>
- [Evaluation cases](artifact/evals/evals.json) <br>
- [Trigger evaluation cases](artifact/evals/trigger_evals.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown analytical report with tables, calculations, sensitivity labels, and action recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include relationship diagrams, decision lineage summaries, confidence labels, and follow-up questions.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
