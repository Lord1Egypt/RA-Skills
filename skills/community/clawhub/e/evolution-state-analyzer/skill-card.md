## Description: <br>
Analyzes the evolution memory graph for stagnation patterns, recurring failures, and success plateaus. Generates actionable insights to guide future evolution cycles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to analyze an OpenClaw evolution memory graph, identify stagnation or recurring failure patterns, and generate recommendations for future evolution cycles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads a local evolution memory graph from its default path or from a caller-supplied path. <br>
Mitigation: Only pass file paths that are intended for analysis and avoid exposing unrelated local files. <br>
Risk: The generated recommendations can be mistaken for commands or authoritative decisions. <br>
Mitigation: Treat recommendations as reviewable guidance and confirm them before changing future evolution cycles. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wanng-ide/evolution-state-analyzer) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [JSON analysis report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes cycle counts, success rates, stagnation status, top genes, top failures, and recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
