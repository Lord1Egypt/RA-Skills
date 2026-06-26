## Description: <br>
Audit-ready decision artifacts for LLM outputs: assumptions, risks, recommendation, and review gating in schema-valid JSON. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abeltennyson](https://clawhub.ai/user/abeltennyson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, decision makers, auditors, and operations teams use this skill to produce structured, reviewable JSON decision records for high-stakes or review-required decisions. It surfaces assumptions, risks, recommendations, clarifications, and consistency checks without claiming outcome certainty. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated decision records can contain sensitive business, legal, medical, financial, or personal details from the prompt. <br>
Mitigation: Store and share generated artifacts only in systems appropriate for the sensitivity of the original decision context. <br>
Risk: Structured recommendations may be mistaken for final authority in high-stakes decisions. <br>
Mitigation: Keep human review for high-stakes decisions and use the artifact as a review aid rather than a replacement for accountable decision-making. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abeltennyson/abe-dgr) <br>
- [DGR homepage](https://www.heybossai.com/skills/dgr) <br>
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [Schema-valid JSON decision record] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include metadata, input summary, assumptions, risks, recommendation, optional clarifications and decomposition, and a consistency check.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
