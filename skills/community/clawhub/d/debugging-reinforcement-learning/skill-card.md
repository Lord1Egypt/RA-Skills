## Description:

Debug non-deterministic agent behavior in reinforcement learning environments with stochasticity control, reproducibility tools, behavior analysis, and reward debugging strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roamer-remote](https://clawhub.ai/user/roamer-remote)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reinforcement learning engineers use this skill to make stochastic experiments reproducible, isolate nondeterminism, inspect policy behavior, and diagnose reward signal problems in Gym/Gymnasium, PettingZoo, and custom environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trajectory records and debug reports may contain sensitive experiment observations, actions, rewards, or environment metadata.

Mitigation: Handle generated reports according to the sensitivity of the experiment data, redact sensitive fields before sharing, and avoid committing raw trajectory captures unless they are approved for disclosure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roamer-remote/skills/debugging-reinforcement-learning)
- [Publisher profile](https://clawhub.ai/user/roamer-remote)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance, JSON, CSV]

**Output Format:** [Markdown guidance, JavaScript code utilities, JSON trajectory/debug objects, CSV-style logs, and structured debug reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated records may include observations, actions, rewards, seeds, RNG states, and environment info supplied by the user's experiment code.]

## Skill Version(s):

1.0.0 (source: evidence.release.version and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
