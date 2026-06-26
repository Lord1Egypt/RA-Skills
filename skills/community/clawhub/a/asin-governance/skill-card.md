## Description: <br>
Asin Governance provides a constraint engine, safety oracle, drift detection, sandbox replay, handshake validation, and audit trails for autonomous agent ecosystems. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dbottrader](https://clawhub.ai/user/dbottrader) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators of autonomous agent stacks use this skill to run pre-action governance checks, validate ASH session handshakes, simulate higher-risk actions, and record audit trails before committing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles credentials, tokens, network access, and local audit data. <br>
Mitigation: Review the heartbeat and handshake components before installation, avoid real Moltbook credentials during evaluation, and keep the exchange server unexposed until token handling and log retention are reviewed. <br>
Risk: Several advertised safety controls are weaker than described, so the skill should not be treated as a hard security boundary. <br>
Mitigation: Use it as prototype governance support with independent review and human approval for high-impact actions. <br>
Risk: The included fuzz report shows multiple mutated payloads passing safety checks. <br>
Mitigation: Strengthen oracle validation and rerun adversarial tests before enabling autonomous posting or profile-changing workflows. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/dbottrader/asin-governance) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Code] <br>
**Output Format:** [Markdown guidance with JSON configuration, Python modules, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local governance checks, session manifests, replay results, and audit records; security-sensitive use requires review before deployment.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact metadata reports 0.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
