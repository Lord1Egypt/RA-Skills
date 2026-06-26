## Description: <br>
Validates executed improvement candidates with a seven-layer gate, routes uncertain changes to human review, and rejects or reverts candidates when required checks fail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lanyasheng](https://clawhub.ai/user/lanyasheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to validate whether completed skill-improvement changes should be kept, reverted, rejected, or queued for human approval. It is intended for closed-loop improvement pipelines that already produce ranking, execution, and optional evaluation artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rollback pointers can change local files when a candidate is rejected, reverted, or escalated. <br>
Mitigation: Run the skill only in the intended improvement-gate pipeline with trusted execution artifacts and a dedicated state root. <br>
Risk: Human review decisions are persisted locally and can affect later promotion decisions. <br>
Mitigation: Restrict access to the review state directory and require reviewer identity and rationale for completed reviews. <br>
Risk: Incorrect or untrusted ranking, execution, or evaluation artifacts can drive the gate toward the wrong decision. <br>
Mitigation: Provide artifacts from trusted upstream skills and inspect pending-promote records before approving changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lanyasheng/auto-improvement-gate) <br>
- [Artifact README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Gate script](artifact/scripts/gate.py) <br>
- [Human review script](artifact/scripts/review.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI commands and JSON receipt examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces gate decisions, rollback status, pending-review records, and next-step guidance through local CLI workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
