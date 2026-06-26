## Description: <br>
Pre-execution governance for high-risk agent actions. Uses persona-weighted consensus to decide ALLOW/BLOCK/REQUIRE_REWRITE before external or irreversible side effects occur, with board-native audit artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent platform teams use this skill as a final pre-execution gate for destructive, external, privileged, or otherwise high-risk agent actions. It returns a deterministic allow, block, or rewrite decision with audit references before side effects occur. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A misconfigured consensus state path or blocking policy could cause the guard to allow, block, or rewrite actions differently than the team expects. <br>
Mitigation: Review CONSENSUS_STATE_FILE, CONSENSUS_STATE_ROOT, and the action blocking policy before relying on the skill in an automation path. <br>
Risk: The skill writes local board and decision artifacts under the configured consensus state path. <br>
Mitigation: Use a scoped writable state directory and monitor generated decision artifacts as part of the workflow audit trail. <br>
Risk: In external_agent mode, externally supplied votes influence the final decision. <br>
Mitigation: Accept external votes only from trusted agents, humans, or models and validate inputs before invoking the guard. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-agent-action-guard) <br>
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [consensus-guard-core repository](https://github.com/kaicianflone/consensus-guard-core) <br>
- [consensus-tools repository](https://github.com/kaicianflone/consensus-tools) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [JSON decision response with board artifact references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ALLOW, BLOCK, or REQUIRE_REWRITE, required follow-up actions, vote aggregation details, and decision artifact references under the configured consensus state path.] <br>

## Skill Version(s): <br>
1.1.14 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
