## Description: <br>
Provides deterministic preflight risk classification for command-like actions, returning allow, require approval, or block decisions with detailed reason codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[parmindersk](https://clawhub.ai/user/parmindersk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill as a local advisory guardrail to classify proposed command-like actions before execution and surface reason codes for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An allow decision only means the command did not match the bundled risk patterns. <br>
Mitigation: Review high-impact commands and tune policy.baseline.json to match the workspace, domains, and sensitive paths where the skill will be used. <br>
Risk: The baseline policy may not reflect a user's actual workspace layout or approval requirements. <br>
Mitigation: Update workspaceRoots, allowlistedDomains, highRiskPatterns, and actions before relying on the classifier for enforcement decisions. <br>


## Reference(s): <br>
- [DeepInspect Guardrails ClawHub release](https://clawhub.ai/parmindersk/deepinspect-openclaw-guardrails) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Guidance, Configuration] <br>
**Output Format:** [JSON decisions with reason codes, plus Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decision values are allow, require_approval, or block; policy behavior is tunable through policy.baseline.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
