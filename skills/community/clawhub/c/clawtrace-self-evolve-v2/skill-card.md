## Description: <br>
Ask Tracy to analyze your recent trajectories and improve your agent behavior based on data-driven recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[richard-epsilla](https://clawhub.ai/user/richard-epsilla) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to ask ClawTrace's Tracy service to review recent trajectory history, identify recurring failures or cost drivers, and suggest behavior improvements for future agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends trajectory context to an external ClawTrace analysis service. <br>
Mitigation: Use it only with a trusted ClawTrace account and require explicit user approval before sending trace or session data. <br>
Risk: External recommendations may influence agent behavior, context trimming, or persistent memory. <br>
Mitigation: Show Tracy's recommendations to the user first and get permission before changing behavior, trimming context, or writing to MEMORY.md. <br>
Risk: Recommendations based on prior trajectories may be incomplete or unsuitable for a current high-stakes task. <br>
Mitigation: Treat recommendations as reviewable guidance and keep existing safety, security, and task-specific constraints in force. <br>


## Reference(s): <br>
- [ClawTrace homepage](https://clawtrace.ai) <br>
- [ClawHub skill page](https://clawhub.ai/richard-epsilla/clawtrace-self-evolve-v2) <br>
- [ClawTrace evolve API endpoint](https://api.clawtrace.ai/v1/evolve/ask) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, API Calls, Markdown] <br>
**Output Format:** [Markdown guidance with Python example code and streamed text responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CLAWTRACE_OBSERVE_KEY and sends questions plus optional trace or session identifiers to ClawTrace.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
