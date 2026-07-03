## Description: <br>
Implements a neuromorphic-quantum anomaly-detection pipeline using LIF spike encoding, contextual bandit allocation, adaptive threshold hot-swapping, and append-only event logging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[evezart](https://clawhub.ai/user/evezart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security or operations engineers can use this skill as a local anomaly-detection simulation for spike encoding, backend allocation, adaptive threshold updates, and event-log replay. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact automatically loads data/qtable_pretrained.pkl if present, and Python pickle files can execute code when loaded. <br>
Mitigation: Use only trusted local qtable files, remove unexpected data/qtable_pretrained.pkl files before running, and review the skill before installation in sensitive workspaces. <br>
Risk: The artifact is a local simulation or demo rather than a validated production anomaly-detection system. <br>
Mitigation: Treat its anomaly decisions and adaptive threshold changes as experimental output until validated against representative data and operational requirements. <br>


## Reference(s): <br>
- [Evez Rqns on ClawHub](https://clawhub.ai/evezart/evez-rqns) <br>
- [Skill overview](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance for agents, with plain text console telemetry and JSON status output when the included Python simulation is run.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The runnable artifact emits per-tick anomaly status, backend selection, latency, energy, learning state, spike counts, event-spine length, and final JSON status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
