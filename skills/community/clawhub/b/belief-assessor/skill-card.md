## Description: <br>
LLM-driven epistemic reasoning engine that evaluates claims against evidence and returns calibrated confidence with a structured belief state. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hqzzdsda](https://clawhub.ai/user/hqzzdsda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to assess whether a claim is trustworthy, identify contradictions across evidence, and quantify uncertainty before presenting or relying on information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Claims and evidence may be sent to external search or LLM tooling during assessment. <br>
Mitigation: Redact private, regulated, proprietary, or personally sensitive material before use, or run the workflow with approved local search and LLM tooling. <br>
Risk: Assessment output may be over-trusted despite low-quality, sparse, stale, or contradictory evidence. <br>
Mitigation: Review the returned confidence_range, veto_reasons, and state before citing the result, and use the conservative preset for high-stakes decisions. <br>


## Reference(s): <br>
- [Belief Assessor ClawHub page](https://clawhub.ai/hqzzdsda/belief-assessor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown guidance with JSON-style assessment results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Assessment results include state, confidence, confidence_range, features, veto_reasons, cap_applied, and summary.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
