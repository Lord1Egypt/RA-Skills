## Description: <br>
Attack a product's observable behavior, or red-team an idea, argument, or plan; a fresh, TDD-independent subagent records only proven, reproducible breakages and never edits the target. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vincentjiang06](https://clawhub.ai/user/vincentjiang06) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and loop owners use this skill to run bounded adversarial rounds against products or ideas and capture only proven, reproducible breakages as handoff records for a separate fix round. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for adversarial testing and may probe live behavior or ideas aggressively if invoked without clear limits. <br>
Mitigation: Use it only on authorized targets, require explicit in-scope and out-of-scope boundaries, and set a bounded attempt and token budget before the attack round starts. <br>
Risk: Self-research or live CLI, HTTP, or app probing could expose sensitive files, secrets, or systems outside the intended test surface. <br>
Mitigation: Exclude secret-bearing paths and sensitive systems up front, keep the scope to the smallest useful surface, and require the documented blast-radius and abort controls. <br>
Risk: A clean verdict can be mistaken for proof that the target is correct. <br>
Mitigation: Treat clean as only no proven break within the declared budget, and increase budget, scope, or oracle strength when higher assurance is needed. <br>
Risk: Unreproduced or weakly supported observations could be misused as confirmed defects. <br>
Mitigation: Accept confirmed findings only when the validator passes and a separate fresh reader re-runs the minimized repro and signs the checklist. <br>


## Reference(s): <br>
- [Skill specification](SKILL.md) <br>
- [English README](README.en.md) <br>
- [Attack process](references/attack-process.md) <br>
- [Context intake](references/context-intake.md) <br>
- [Oracle menu](references/oracle-menu.md) <br>
- [Loop and metrics](rules/loop-and-metrics.md) <br>
- [Attack record schema](schemas/attack-record.schema.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown handoff documents with JSON or JSONL attack records and inline shell validation commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are bounded by the declared attack budget and token cap; confirmed findings require reproducible proof, a named oracle, and fresh-reader verification.] <br>

## Skill Version(s): <br>
0.3.2 (source: server release metadata and changelog, released 2026-06-23) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
