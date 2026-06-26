## Description: <br>
Pre-deployment governance for release and infrastructure rollout requests. Use when an agent or workflow proposes shipping code/config/infrastructure changes to staging or production and you need deterministic ALLOW/BLOCK/REQUIRE_REWRITE decisions with strict schema validation, idempotency, and board-native audit artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, release engineers, and agent-assisted CI/CD workflows use this skill to evaluate proposed code, configuration, or infrastructure deployments before rollout. It returns deterministic ALLOW, BLOCK, or REQUIRE_REWRITE decisions and records audit artifacts under the configured state path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can gate real deployment decisions and may block or require rewrites for rollout requests. <br>
Mitigation: Decide before installation whether it is advisory or authoritative, and require human review before enforcing it in production CI/CD. <br>
Risk: Decision artifacts are written to paths resolved from CONSENSUS_STATE_ROOT and CONSENSUS_STATE_FILE. <br>
Mitigation: Use a dedicated protected state directory, avoid system or secrets paths, run as a non-root user, and scope writable mounts. <br>
Risk: External votes can influence deployment decisions in external_agent mode. <br>
Mitigation: Accept external_votes only from authenticated trusted systems and keep minimal runtime environment access. <br>
Risk: The skill depends on consensus-guard-core for aggregation and state helpers. <br>
Mitigation: Pin dependencies, review consensus-guard-core, and audit the lockfile before CI/CD use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-deployment-guard) <br>
- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [consensus-guard-core source](https://github.com/kaicianflone/consensus-guard-core) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [json, files, guidance] <br>
**Output Format:** [JSON decision payload with board audit artifact writes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns ALLOW, BLOCK, or REQUIRE_REWRITE with policy flags, votes, aggregation details, required actions, and board write references.] <br>

## Skill Version(s): <br>
0.1.10 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
