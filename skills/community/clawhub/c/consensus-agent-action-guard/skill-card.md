## Description:

Pre-execution governance for high-risk agent actions. Uses persona-weighted consensus to decide ALLOW/BLOCK/REQUIRE_REWRITE before external or irreversible side effects occur, with board-native audit artifacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kaicianflone](https://clawhub.ai/user/kaicianflone)

### License/Terms of Use:

MIT

## Use Case:

Developers and automation teams use this skill to gate destructive operations, privileged tool use, outbound communication, and other high-risk agent actions before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact decisions can be driven by weakly validated caller input.

Mitigation: Authenticate external votes, enforce schema validation, and apply conservative action metadata before relying on the decision.

Risk: The skill may be placed in automation paths that can delete data, post publicly, send messages, or mutate business systems.

Mitigation: Review deployment carefully and require human confirmation for irreversible or high-risk actions.

Risk: Dependency drift can change the guard behavior after installation.

Mitigation: Install with the committed package-lock file and review dependency updates before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kaicianflone/skills/consensus-agent-action-guard)
- [Publisher profile: kaicianflone](https://clawhub.ai/user/kaicianflone)
- [consensus-guard-core npm package](https://www.npmjs.com/package/consensus-guard-core)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [json, guidance, configuration]

**Output Format:** [JSON decision object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes final_decision, vote aggregation, required_actions, and board_writes references.]

## Skill Version(s):

1.1.14 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
