## Description:

Ask Tracy to analyze your recent trajectories and improve your agent behavior based on data-driven recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard-epsilla](https://clawhub.ai/user/richard-epsilla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to ask ClawTrace for analysis of recent trajectories after costly runs, failures, repeated issues, or session wrap-up. The skill helps identify patterns in cost, reliability, context management, and tool-call efficiency before the agent applies reviewed improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends trajectory-linked questions and optional trace or session identifiers to ClawTrace.

Mitigation: Use it only when that data sharing is acceptable, and avoid including sensitive task details beyond what is needed for analysis.

Risk: The skill asks the agent to immediately apply and persist external recommendations.

Mitigation: Review each recommendation before changing agent behavior or writing to MEMORY.md.

Risk: Each ClawTrace call may consume credits.

Mitigation: Follow the artifact's limit of no more than two calls per session unless a new failure occurs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard-epsilla/skills/clawtrace-self-evolve-v2)
- [ClawTrace homepage](https://clawtrace.ai)
- [ClawTrace evolve API endpoint](https://api.clawtrace.ai/v1/evolve/ask)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown guidance with Python code snippets and streamed text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAWTRACE_OBSERVE_KEY and may use question, trace_id, and session_id values when calling ClawTrace.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
