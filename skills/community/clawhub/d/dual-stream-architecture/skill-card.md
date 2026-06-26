## Description: <br>
Dual-stream event publishing combining Kafka for durability with Redis Pub/Sub for real-time delivery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wpank](https://clawhub.ai/user/wpank) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to design event-driven systems that need both durable event replay through Kafka and low-latency live updates through Redis Pub/Sub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with production Kafka or Redis credentials could implement or operate event systems with real infrastructure access. <br>
Mitigation: Grant production Kafka or Redis credentials only when the agent is explicitly authorized to implement or operate those systems. <br>


## Reference(s): <br>
- [Dual Stream Architecture on ClawHub](https://clawhub.ai/wpank/dual-stream-architecture) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Go and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes architecture guidance, channel naming conventions, batch publishing examples, decision criteria, and edge case handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
