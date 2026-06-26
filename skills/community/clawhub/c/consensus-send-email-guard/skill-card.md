## Description: <br>
Persona-weighted pre-send email governance for AI systems that returns APPROVE, BLOCK, or REWRITE decisions and writes decision artifacts to a board ledger. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and automation teams use this skill to review outbound email drafts before send-time actions, especially for customer-facing, sales, policy, or other high-trust communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reviewed email drafts and decision records may be stored in local audit artifacts. <br>
Mitigation: Use the skill only where local audit storage is acceptable, and configure a dedicated non-shared state directory. <br>
Risk: Misconfigured state-path environment variables could write audit data to sensitive, shared, or system locations. <br>
Mitigation: Set CONSENSUS_STATE_FILE and CONSENSUS_STATE_ROOT to non-privileged paths that do not contain secrets or system data. <br>
Risk: Production installs can drift if dependencies are resolved nondeterministically. <br>
Mitigation: Use deterministic installs from the provided lockfile when deploying the skill in production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-send-email-guard) <br>
- [Non-NVIDIA publisher profile](https://clawhub.ai/user/kaicianflone) <br>
- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [consensus-guard-core related source](https://github.com/kaicianflone/consensus-guard-core) <br>
- [consensus-tools related source](https://github.com/kaicianflone/consensus-tools) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text, guidance, configuration] <br>
**Output Format:** [Strict machine-parseable JSON containing decision metadata, vote aggregation, final_decision, optional rewrite_patch, and board write references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local decision artifacts under the configured consensus state path.] <br>

## Skill Version(s): <br>
1.1.15 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
