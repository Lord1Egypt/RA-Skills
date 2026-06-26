## Description: <br>
Context window is near capacity, causing the model to drop earlier content silently and produce degraded, partial, or inconsistent output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mvogt99](https://clawhub.ai/user/mvogt99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and their operators use this skill to recognize context-window saturation and choose practical ways to split, summarize, or restart work so responses stay grounded in the relevant context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Summaries or compressed context can omit important requirements or details. <br>
Mitigation: Review summaries of important instructions or documents before relying on them, and re-inject critical source material when needed. <br>
Risk: Context-window saturation can cause incomplete or inconsistent agent output without an explicit error. <br>
Mitigation: Split large tasks into stages, keep only the context needed for the current step, and start a fresh session when prior context is no longer useful. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/mvogt99/context-near-overflow) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text] <br>
**Output Format:** [Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution or external tool access; provides context-management recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
