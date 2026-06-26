## Description: <br>
Analyze text and return a sentiment score from -1 (negative) to +1 (positive) using Expanso Edge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aronchick](https://clawhub.ai/user/aronchick) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to classify submitted text as positive, negative, or neutral and receive a numeric sentiment score and confidence value. It supports local CLI scoring and an HTTP server mode for service-style use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted text may be sent to OpenAI when the OpenAI-backed scoring path is used. <br>
Mitigation: Avoid submitting secrets, proprietary text, personal data, or regulated content, and install only if this data flow is acceptable. <br>
Risk: Server mode can expose the scoring endpoint to reachable network clients without visible access controls. <br>
Mitigation: Prefer CLI mode for local user-directed scoring; when running server mode, bind it to a trusted interface or place it behind authentication and rate limits. <br>
Risk: Remote scoring can create OpenAI usage and cost exposure. <br>
Mitigation: Monitor OpenAI usage and apply operational controls appropriate for the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aronchick/expanso-sentiment-score) <br>
- [README.md](README.md) <br>
- [SKILL.md](SKILL.md) <br>
- [skill.yaml](skill.yaml) <br>
- [pipeline-cli.yaml](pipeline-cli.yaml) <br>
- [pipeline-mcp.yaml](pipeline-mcp.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [JSON object with score, label, confidence, and metadata fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Score ranges from -1 to +1; label is positive, negative, or neutral.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
