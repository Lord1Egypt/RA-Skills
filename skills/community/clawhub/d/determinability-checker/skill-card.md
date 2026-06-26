## Description: <br>
Causal Sufficiency Determinability Checker - Meta-Skill Gatekeeper based on JEP Paper CheckDeterminability Algorithm. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[schchit](https://clawhub.ai/user/schchit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to check whether a target judgment is zero-error determinable from a finite set of observed configurations before proceeding with an action. When evidence is insufficient, it returns a counterexample and missing-evidence guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The proceed/not-proceed result could be over-trusted for high-impact workflows. <br>
Mitigation: Use the result as advisory evidence and require human or policy review before automatic approval of sensitive actions. <br>
Risk: Running the FastAPI service on an unintended network interface could expose the checker to unwanted requests. <br>
Mitigation: Bind the service only to the intended interface and deploy it inside an isolated Python environment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/schchit/determinability-checker) <br>
- [README](artifact/determinability-checker-skill/README.md) <br>
- [CHANGELOG](artifact/determinability-checker-skill/CHANGELOG.md) <br>
- [Skill manifest](artifact/determinability-checker-skill/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, Guidance] <br>
**Output Format:** [JSON response with determinability status, decision table or counterexample, and missing-evidence guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The HTTP API returns a structured response for a single check request.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata, frontmatter, manifest, and changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
