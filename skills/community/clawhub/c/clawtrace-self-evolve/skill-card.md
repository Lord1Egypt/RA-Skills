## Description:

Ask Tracy to analyze your recent trajectories and improve your agent behavior based on data-driven recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard-epsilla](https://clawhub.ai/user/richard-epsilla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to ask ClawTrace for analysis of recent trajectory failures, costs, context growth, and tool-call patterns, then apply concise recommendations to improve future runs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An external analysis service can shape current and future agent behavior through recommendations based on trajectory data.

Mitigation: Require explicit approval before applying each recommendation, and reject changes to safety rules or unrelated goals.

Risk: Trajectory data may contain sensitive task, prompt, or tool-output content.

Mitigation: Redact sensitive trace content where possible before analysis and install only when ClawTrace trajectory analysis is acceptable.

Risk: Persisting recommendations to MEMORY.md can carry incorrect or inappropriate guidance into later sessions.

Mitigation: Review every MEMORY.md entry before it is written and keep entries narrow, factual, and tied to observed behavior.

## Reference(s):

- [ClawTrace](https://clawtrace.ai)
- [ClawTrace Evolve API endpoint](https://api.clawtrace.ai/v1/evolve/ask)
- [ClawHub skill page](https://clawhub.ai/richard-epsilla/skills/clawtrace-self-evolve)
- [Publisher profile](https://clawhub.ai/user/richard-epsilla)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with Python code examples and API request instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWTRACE_OBSERVE_KEY and may produce recommendations for current-session behavior and future memory notes.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
