## Description: <br>
Detects and records capability gaps, repeated failure patterns, rule conflicts, user corrections, and workaround cases so future sessions can prioritize skill or rule improvements. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dottythehomeless](https://clawhub.ai/user/dottythehomeless) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent hits a capability boundary, repeats a mistake, encounters a rule conflict, or uses a workaround. It guides the agent to write a structured memory note that future sessions can scan and convert into skill drafts, tool additions, or rule fixes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Capability-gap notes may persist sensitive details if the agent records secrets, private personal details, customer data, or sensitive operational context. <br>
Mitigation: Review memory entries before relying on or sharing them, and avoid recording secrets or sensitive operational details. <br>
Risk: Improvement signals can be incomplete or misleading if they are based on a single failed interaction. <br>
Mitigation: Use the recorded impact and repetition fields to prioritize follow-up, and review proposed skill or rule changes before deployment. <br>


## Reference(s): <br>
- [Capability Radar on ClawHub](https://clawhub.ai/dottythehomeless/capability-radar) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance, text] <br>
**Output Format:** [Markdown memory entry using a fixed field list] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes persistent capability-gap notes to local memory when the host agent permits file edits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
