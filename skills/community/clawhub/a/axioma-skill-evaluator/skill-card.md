## Description: <br>
Axioma Skill Evaluator evaluates OpenClaw skills before publication or improvement using an Axioma five-dimension rubric and an ISO 25010 checklist with bundled Python scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kofna3369](https://clawhub.ai/user/kofna3369) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit OpenClaw skill folders, generate automated and manual quality scores, and identify publication-readiness issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The evaluator writes reports to hard-coded personal filesystem paths. <br>
Mitigation: Run it only in a reviewed local workspace and patch or redirect report paths before relying on generated output. <br>
Risk: The bundled reports may contain misleading threshold contradictions. <br>
Mitigation: Treat scores as advisory and manually verify thresholds, findings, and approval decisions. <br>
Risk: The broad scan mode uses hard-coded scan roots. <br>
Mitigation: Run evaluations on explicit skill folders and avoid broad scan mode unless the configured roots have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kofna3369/axioma-skill-evaluator) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [Axioma evaluator script](artifact/evaluator.py) <br>
- [ISO 25010 evaluation script](artifact/eval-skill.py) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Terminal text reports, optional JSON, and Markdown guidance with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces advisory local evaluation results that require manual review before release decisions.] <br>

## Skill Version(s): <br>
2.2.0 (source: ClawHub release metadata; artifact body lists 2.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
