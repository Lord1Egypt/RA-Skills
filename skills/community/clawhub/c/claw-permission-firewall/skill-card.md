## Description: <br>
Evaluates agent actions for security risks, enforcing least-privilege policies with allow, deny, or confirmation decisions and secret redaction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bharathjanumpally](https://clawhub.ai/user/bharathjanumpally) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to evaluate proposed HTTP, file, and command actions before execution. It returns a policy decision, redacted action data, risk reasons, and an audit record so the host agent can allow, deny, or request confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Policy evaluation can be mistaken for a complete security boundary. <br>
Mitigation: Use it as a policy gate, configure policy.yaml for the deployment environment, and fail closed for unknown action types. <br>
Risk: Executing the original action instead of the returned sanitizedAction can bypass redaction and policy normalization. <br>
Mitigation: Only execute sanitizedAction values after an ALLOW decision. <br>
Risk: Confirmation decisions depend on a trusted host layer. <br>
Mitigation: Keep user confirmation outside the skill in a trusted interface and re-run evaluation with confirmed context before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bharathjanumpally/claw-permission-firewall) <br>
- [Publisher profile](https://clawhub.ai/user/bharathjanumpally) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [README](artifact/README.md) <br>
- [Default policy](artifact/policy.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [json, guidance, configuration] <br>
**Output Format:** [JSON decision object with risk reasons, sanitized action data, optional confirmation prompt, and audit record] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Policy-driven ALLOW, DENY, or NEED_CONFIRMATION response; secrets are redacted from returned actions where policy rules match.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version, package.json, CHANGELOG.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
