## Description:

Bridge is an Agent-to-Human (A2H) verification and escrow platform for requesting physical-world tasks, defining proof criteria, splitting work into milestones, tracking worker reputation, and handling disputes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Bridge to prototype agent-mediated physical-world task requests with criteria-based proof checks, milestone release logic, disputes, and worker reputation tracking.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the current release is weak for money- or reputation-affecting physical-task escrow and verification use.

Mitigation: Use it only in controlled evaluation until authentication, authorization, real settlement, durable storage, privacy controls, and trusted proof verification are added.

Risk: Task, escrow, dispute, and worker reputation records are held in process memory.

Mitigation: Add durable storage, audit logs, and reconciliation before relying on any task outcome, balance, or reputation score.

Risk: Proof checks rely on submitted request data for GPS, photo hashes, timestamps, signatures, and witness attestations.

Mitigation: Require trusted capture, identity binding, anti-tamper validation, and human dispute review before acting on verification results.

## Reference(s):

- [Bridge ClawHub skill page](https://clawhub.ai/mirni/skills/a2h-bridge)
- [mirni publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, curl examples, and JSON request bodies.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes local FastAPI server instructions and example HTTP requests for task creation, verification, disputes, milestones, workers, platforms, and statistics.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
