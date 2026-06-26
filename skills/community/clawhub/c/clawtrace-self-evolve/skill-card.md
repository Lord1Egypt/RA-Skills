## Description: <br>
Ask Tracy to analyze recent ClawTrace trajectories and return data-driven recommendations for improving agent behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard-epsilla](https://clawhub.ai/user/richard-epsilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to ask ClawTrace for analysis of recent runs, failures, cost spikes, and recurring tool or context issues, then apply the resulting recommendations to future agent behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends trajectory-analysis requests to ClawTrace, which may include sensitive run history. <br>
Mitigation: Use it only when the operator trusts ClawTrace with trajectory data, redact sensitive trace content where possible, and require explicit approval before API calls. <br>
Risk: The skill asks the agent to immediately change behavior and write persistent memory based on returned recommendations. <br>
Mitigation: Review recommendations and any proposed MEMORY.md entry before applying or storing them. <br>


## Reference(s): <br>
- [ClawTrace homepage](https://clawtrace.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Markdown, Code] <br>
**Output Format:** [Markdown guidance with Python API-call examples and recommendation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWTRACE_OBSERVE_KEY and sends trajectory-analysis requests to ClawTrace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
