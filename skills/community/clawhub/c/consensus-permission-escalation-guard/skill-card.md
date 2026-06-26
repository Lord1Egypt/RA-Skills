## Description: <br>
Pre-execution governance for IAM and permission escalation changes that returns deterministic ALLOW, BLOCK, or REQUIRE_REWRITE decisions with strict schema validation, idempotency, and audit artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, platform engineers, and security reviewers use this skill to evaluate proposed IAM grants, scope expansions, role assumptions, and break-glass access before execution. It helps turn escalation requests into deterministic governance decisions and replayable audit records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audit state is written to a configured filesystem path, which can create exposure if pointed at sensitive or system directories. <br>
Mitigation: Use a dedicated non-privileged state directory, run as a non-root user, and constrain filesystem permissions. <br>
Risk: An ALLOW decision may be mistaken for automatic authorization of sensitive production changes. <br>
Mitigation: Treat ALLOW as a governance signal and retain human or procedural approval for high-impact permission changes. <br>
Risk: The runtime depends on consensus-guard-core and transitive dependencies as part of the trust boundary. <br>
Mitigation: Review and pin dependencies, keep the lockfile audited, and test in an isolated environment before production promotion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-permission-escalation-guard) <br>
- [README](artifact/README.md) <br>
- [Security Assurance Note](artifact/SECURITY-ASSURANCE.md) <br>
- [Input schema](artifact/spec/input.schema.json) <br>
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [JSON decision object with optional JSON audit artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Decision values are ALLOW, BLOCK, or REQUIRE_REWRITE; runtime artifacts are written under the configured consensus state path.] <br>

## Skill Version(s): <br>
0.1.13 (source: server release and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
