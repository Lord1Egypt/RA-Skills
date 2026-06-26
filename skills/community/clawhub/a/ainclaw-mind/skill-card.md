## Description: <br>
Save up to 90% on Token costs. One agent explores, all agents benefit. Cloud-cached workflows with zero inference cost. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ainclaw](https://clawhub.ai/user/ainclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use ClawMind to check a cloud workflow cache before LLM exploration, replay matching Lobster workflows, and contribute sanitized successful traces for future reuse. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task and browser-session context may be sent to the configured cloud endpoint. <br>
Mitigation: Review the endpoint and trust model before use; avoid sensitive, logged-in, private, or internal sites unless the endpoint is trusted. <br>
Risk: Cloud-supplied cached workflows may act in the browser without clear per-use approval. <br>
Mitigation: Require review of cached workflows before execution and keep normal fallback behavior available when validation or trust checks fail. <br>
Risk: Successful workflows may be contributed automatically. <br>
Mitigation: Disable auto_contribute for sensitive work or where sharing workflow patterns is not acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ainclaw/ainclaw-mind) <br>
- [Skill Documentation](SKILL.md) <br>
- [README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Text responses with configuration values and cached workflow execution results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute cached browser workflows through Lobster and send sanitized workflow data to a configured cloud endpoint.] <br>

## Skill Version(s): <br>
1.0.5 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
