## Description:

Run a two-agent collaborative problem-solving workflow where one agent is your OpenClaw agent and a second agent challenges assumptions, surfaces risks, improves the plan over multiple rounds, outputs one merged actionable solution, and stores it in Open Brain memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tvaloki](https://clawhub.ai/user/tvaloki)

### License/Terms of Use:


## Use Case:

Developers and engineers use DualAgentSolver when they want an OpenClaw primary solver and a second critic agent to iteratively challenge a problem-solving plan and produce a merged actionable solution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full run data is automatically stored in Open Brain memory.

Mitigation: Use the skill only for non-sensitive problems unless stored run data is acceptable, and review or delete stored memories after sensitive runs.

Risk: Generated critic inputs can be sent to OpenAI when OPENAI_API_KEY is set.

Mitigation: Unset OPENAI_API_KEY for local OpenClaw-only critic behavior, or avoid sending sensitive problem content.

Risk: The security verdict is suspicious and calls for review before installation.

Mitigation: Review the skill before installing and confirm the memory and external API behavior fit the intended environment.

## Reference(s):

- [DualAgentSolver ClawHub skill page](https://clawhub.ai/tvaloki/skills/dual-agent-solver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON object containing round-by-round solver and critic outputs, a final merged solution, memory write result, and memory key]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists the run outcome to Open Brain memory and may include generated implementation plans, risks, rollback guidance, and next actions.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
