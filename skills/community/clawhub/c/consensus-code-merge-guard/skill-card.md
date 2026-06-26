## Description: <br>
Persona-weighted merge governance for AI-assisted engineering. Evaluates PR risk (tests, security markers, reliability signals), returns MERGE/BLOCK/REVISE decisions, and records board-native audit artifacts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaicianflone](https://clawhub.ai/user/kaicianflone) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineering teams use this skill after CI checks and before merge automation to make policy-backed MERGE, BLOCK, or REVISE decisions for pull requests and release branches. It supports persona-weighted voting or externally supplied votes and records auditable decision artifacts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local decision state can affect merge governance if the configured consensus state path is shared or writable by untrusted users. <br>
Mitigation: Use project-scoped consensus state paths and restrict write access to trusted automation or maintainers. <br>
Risk: External votes can influence MERGE, BLOCK, or REVISE outcomes when external_agent mode is used. <br>
Mitigation: Restrict who can supply external votes and validate vote inputs before invoking the guard. <br>
Risk: Dependency changes could alter guard behavior over time. <br>
Mitigation: Honor the package lockfile and run the normal dependency-audit process in CI. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kaicianflone/consensus-code-merge-guard) <br>
- [Publisher profile](https://clawhub.ai/user/kaicianflone) <br>
- [consensus-guard-core package](https://www.npmjs.com/package/consensus-guard-core) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>
- [OpenClaw repository](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Guidance] <br>
**Output Format:** [JSON decision response with decision status, vote aggregation, required actions, and board artifact references.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local decision audit artifacts under the configured consensus state path.] <br>

## Skill Version(s): <br>
1.1.15 (source: server release evidence and package.json; SKILL.md frontmatter lists 1.1.14) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
