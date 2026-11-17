## Description:

Implements a neuromorphic-style anomaly detection pipeline using LIF spike encoding, contextual bandit backend allocation, and adaptive threshold updates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers can use this skill as a local anomaly-detection pipeline that simulates signal sensing, backend allocation, solver feedback, and adaptive threshold updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local data/qtable_pretrained.pkl file can execute attacker-controlled code if loaded with pickle.

Mitigation: Review the working directory before running the skill, do not run it where untrusted pickle files may exist, and replace pickle loading with a non-executable model format before production use.

Risk: The event log and generated sensor output are demo-quality telemetry and should not be treated as tamper-evident security evidence.

Mitigation: Use the logged events for development visibility only unless independent integrity controls and production telemetry validation are added.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/evezart/skills/evez-rqns)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local simulation output, anomaly metrics, backend-routing decisions, learning updates, and event-log status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
