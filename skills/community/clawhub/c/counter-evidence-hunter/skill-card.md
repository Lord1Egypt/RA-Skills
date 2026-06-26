## Description: <br>
Counter Evidence Hunter helps an agent pressure-test a main conclusion by searching for counter-evidence, flip conditions, alternative explanations, and confidence gaps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z1one0415](https://clawhub.ai/user/z1one0415) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, researchers, and decision-support agents use this skill after forming a mainline claim to find contradictory evidence, conditions that could overturn the conclusion, and alternative explanations before high-stakes analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Confidential claims or private business details may be exposed when the agent uses them as search queries. <br>
Mitigation: Use sanitized summaries or public-safe identifiers when search tools are enabled, and avoid including confidential details in the mainline claim or counter goal. <br>
Risk: Weak or noisy counter-evidence may be over-weighted and distort the final conclusion. <br>
Mitigation: Treat the output as advisory, preserve the skill's hard/soft/noise ratings, and require source review before changing the main analysis. <br>


## Reference(s): <br>
- [Counter-Evidence Patterns](references/counter-patterns.md) <br>
- [Flip Condition Examples](references/flip-condition-examples.md) <br>
- [Counter-Evidence Search Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance] <br>
**Output Format:** [Structured JSON with counter queries, counter-evidence, flip conditions, alternative supports, and confidence assessment fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include dynamic search queries, evidence-strength ratings, blind spots, and 0-100 confidence scoring.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
