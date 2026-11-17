## Description:

Coordinates Planner, Coder, Checker, and Memowriter agents through a gated sprint loop for contract-driven implementation, competing solutions, quality review, and documentation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wljmmx](https://clawhub.ai/user/wljmmx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to route multi-file or test-sensitive coding tasks through a structured multi-agent workflow. It defines sprint contracts, Workboard handoffs, gated review, retry limits, and documentation handoff for implementation work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill auto-routes development work to fixed QQ agent sessions, which can dispatch work outside the intended user's controlled environment.

Mitigation: Install only in environments where the user controls the listed QQ agent sessions and Workboard/Ollama setup; otherwise require user-configured session destinations and explicit approval before cross-session dispatch.

Risk: Multi-agent loops can continue across long-running tasks and repeated retries without ordinary fixed execution timeouts.

Mitigation: Keep Workboard heartbeat, retry limits, blocked-state handling, and human-intervention gates enabled so stalled or repeatedly failing work is surfaced for review.

Risk: The release security verdict is suspicious because cross-session dispatch lacks clear per-task consent in the provided evidence.

Mitigation: Limit which repositories or tasks can trigger the loop and require explicit user consent before dispatching work to configured agents.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wljmmx/skills/competitive-agent-loop)
- [Source skill definition](artifact/SKILL.md)
- [Sprint contract template](artifact/templates/sprint-contract.yaml)
- [REST API workflow example](artifact/examples/rest-api-example.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, YAML sprint-contract templates, and structured review JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes work through external agent sessions and Workboard state; long-running tasks rely on heartbeat and explicit completion or block status.]

## Skill Version(s):

2.0.1 (source: server release metadata and skill heading)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
