## Description: <br>
Meta-skill for AI agent self-improvement that analyzes runtime logs to detect error patterns, regressions, and inefficiencies, then generates structured improvement proposals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sinasu](https://clawhub.ai/user/sinasu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze structured runtime logs, compute health signals, and generate prioritized improvement proposals for agent reliability and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The package metadata requests crypto, purchase, and sensitive credential capabilities that are not clearly needed for the local log-analysis behavior described by the artifact. <br>
Mitigation: Verify the exact publisher, slug, and version before installation, and do not grant purchase, crypto, or credential permissions unless the publisher clearly explains why they are required. <br>
Risk: Runtime logs submitted for analysis may contain secrets, credentials, personal data, or other sensitive operational details. <br>
Mitigation: Redact secrets and sensitive data before submitting logs, and constrain invocation to explicit log-analysis requests. <br>
Risk: Generated recommendations may be incomplete or unsuitable for a production system without engineering review. <br>
Mitigation: Review recommendations before applying them and scan any resulting changes before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sinasu/capability-evolver-pro-bak) <br>
- [Claw0x capability page](https://claw0x.com/skills/capability-evolver) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Guidance, JSON] <br>
**Output Format:** [JSON objects with structured analysis results, health scores, recommendations, evolution proposals, and status metadata] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Analyze and evolve actions require a non-empty logs array; artifact behavior limits results to 50 patterns and 20 recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
