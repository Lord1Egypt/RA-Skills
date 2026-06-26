## Description: <br>
Advocatus gives agents a structured adversarial-review workflow for recording, tracking, and evaluating opposition to doctrines, rules, skills, and assumptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ironiclawdoctor-design](https://clawhub.ai/user/ironiclawdoctor-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and governance reviewers use this skill to capture steelmanned objections, maintain an opposition docket, and run local checks on whether doctrines or rules have addressed recorded challenges. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changes to the opposition registry or DOCTRINES dictionary can alter governance records. <br>
Mitigation: Treat those edits as governance changes and review them before relying on the docket. <br>
Risk: Generated results may be used in downstream decisions about whether doctrines or rules have survived opposition. <br>
Mitigation: Review generated results files before using them to support downstream decisions. <br>
Risk: The evaluator depends on manually maintained registry entries and doctrine metadata staying aligned. <br>
Mitigation: Keep the registry and DOCTRINES dictionary synchronized when adding or updating opposition entries. <br>


## Reference(s): <br>
- [Opposition Registry](references/opposition-registry.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/ironiclawdoctor-design/advocatus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON evaluation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The local evaluator writes timestamped results files under results/ when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
