## Description: <br>
Audits software, agent, workflow, platform, and socio-technical system architectures through engineering cybernetics: stability, feedback loops, noise, delay, error control, damping, observability, adaptation, and safe evolution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xb19960921](https://clawhub.ai/user/xb19960921) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, architects, platform teams, and agent-system builders use this skill to review system behavior over time, diagnose instability, and choose prioritized improvements for feedback, damping, observability, adaptation, and safety boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Architecture reviews may include secrets, credentials, or sensitive production logs in user-provided context. <br>
Mitigation: Use anonymized diagrams, summarized metrics, and redacted logs unless the user intentionally wants the model to process sensitive material. <br>
Risk: Generated architecture guidance may be incorrect or too abstract for the user's actual system constraints. <br>
Mitigation: Review recommendations against the real architecture and verify proposed gates, feedback loops, and safety boundaries before operational changes. <br>


## Reference(s): <br>
- [Control Principles](references/control-principles.md) <br>
- [AgentOS / Multi-Agent Review Rubric](references/agentos-review-rubric.md) <br>
- [ClawHub skill page](https://clawhub.ai/xb19960921/control-mirror) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured review sections, scorecards, prioritized actions, and verification criteria] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces diagnostic architecture-review guidance; users should avoid pasting secrets, credentials, or sensitive production logs unless intended for model processing.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
