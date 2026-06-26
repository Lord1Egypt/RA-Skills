## Description: <br>
Builds and audits trust policies for browser and computer-use agents before they take real-world actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[stevojarvisai-star](https://clawhub.ai/user/stevojarvisai-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and governance reviewers use this skill to evaluate browser-agent policies and proposed actions before live execution, especially for domain allowlists, sensitive-action approval gates, and audit evidence. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy or action JSON used for browser-agent reviews could include sensitive operational data. <br>
Mitigation: Keep policy and action JSON files inside the skill directory and avoid placing real secrets in those files. <br>
Risk: A REVIEW or BLOCK result may indicate that a proposed browser action lacks required controls before live execution. <br>
Mitigation: Review generated REVIEW or BLOCK results before allowing a browser agent to take live actions. <br>
Risk: Irreversible actions may be proposed without explicit approval or pre-action evidence. <br>
Mitigation: Require human approval for sensitive actions and capture screenshot or state evidence before irreversible clicks. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/stevojarvisai-star/browser-agent-trust-hub) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON trust-report fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces ALLOW, REVIEW, or BLOCK verdicts with findings, scores, and required controls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
