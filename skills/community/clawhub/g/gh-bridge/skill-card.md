## Description:

Bridge provides an Agent-to-Human verification API where agents create physical-world tasks, define proof criteria, submit evidence, and receive escrow status decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirni](https://clawhub.ai/user/mirni)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Bridge to prototype human task requests that require GPS, photo, timestamp, or signature-style proof before a simulated escrow status changes. Server security guidance limits this release to local demo use unless production controls are added.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes escrow and proof verification in terms that could be mistaken for production-ready financial custody or real-world attestation.

Mitigation: Use it only as a local demo unless real payment custody, strong proof attestation, authentication, authorization, privacy controls, and durable storage are added.

Risk: Task, proof, and dispute state is in memory and can be lost when the server restarts.

Mitigation: Add durable storage and audit logging before using Bridge for meaningful work assignment or payment decisions.

Risk: Proof checks accept submitted coordinates, photo hashes, timestamps, and non-empty signatures without independent attestation.

Mitigation: Require trusted capture, signature validation, anti-tamper controls, and human review for sensitive physical-world evidence.

Risk: The demo API does not show authentication or authorization around task creation, proof submission, disputes, or stats.

Mitigation: Add identity, authorization checks, rate limits, and access controls before exposing the service beyond a local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirni/skills/gh-bridge)
- [Publisher profile](https://clawhub.ai/user/mirni)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, JSON, Code, Configuration]

**Output Format:** [Markdown guidance with shell commands, curl examples, and JSON API payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local FastAPI server usage guidance and structured API responses for task, verification, dispute, platform, and statistics endpoints.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
