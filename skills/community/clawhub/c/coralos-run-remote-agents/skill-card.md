## Description:

End-to-end Coral Cloud workflow to discover registry remote agents, compose and launch a session of agents, then monitor and close it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[omni-georgio](https://clawhub.ai/user/omni-georgio)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to discover Coral Cloud registry agents, compose strict session payloads, launch remote agent sessions, and monitor lifecycle state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to create, monitor, or close Coral Cloud sessions through external API calls.

Mitigation: Review session payloads before submission and require confirmation for state-changing actions such as creating or closing sessions.

Risk: The skill references helper scripts and payload templates that may affect remote session behavior.

Mitigation: Run only trusted helper scripts and inspect referenced payload templates before using them with a live Coral Cloud environment.

## Reference(s):

- [Coral Cloud API guide](https://docs.coralos.ai/cloud/using-api)
- [CoralOS ClawHub skill page](https://clawhub.ai/omni-georgio/skills/coralos-run-remote-agents)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, HTTP endpoints, payload requirements, and lifecycle checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead the agent to make external Coral Cloud API calls and review session payloads before submission.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
