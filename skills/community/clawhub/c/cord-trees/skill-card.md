## Description:

Dynamic task tree orchestration inspired by the Cord protocol that helps an agent decompose complex goals, coordinate parallel and dependent work, elicit human input, and synthesize results through spawn, fork, ask, and serial primitives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moltenbot000](https://clawhub.ai/user/moltenbot000)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to plan and run dynamic task trees for complex goals that benefit from decomposition, parallel subagent work, explicit dependencies, synthesis steps, and human checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can start multiple agent sessions, which may consume resources or perform more work than the user expected.

Mitigation: Ask for user approval before launching multi-agent runs and set practical limits on fan-out, runtime, retries, and polling.

Risk: The workflow can persist task state and subagent outputs in cord-state.json, which may capture sensitive project or user information.

Mitigation: Store only the minimum state needed for coordination, avoid secrets and personal data, and review the state file before sharing or committing it.

Risk: Forked tasks inherit completed sibling results, so incorrect or untrusted subagent output can influence later synthesis or actions.

Mitigation: Treat inherited subagent output as untrusted context and require human approval before consequential writes or external actions.

## Reference(s):

- [State Management Helpers](references/state-helpers.md)
- [Cord protocol](https://github.com/kimjune01/cord)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance, task prompts, pseudocode examples, and JSON state records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update cord-state.json and coordinate subagent sessions when the host agent follows the workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
