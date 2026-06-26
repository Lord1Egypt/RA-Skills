## Description: <br>
Automatically assesses task complexity for each user message and guides the agent to adjust reasoning depth before answering complex questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cxz9909](https://clawhub.ai/user/cxz9909) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill as an always-on pre-processing checklist to decide when deeper reasoning is warranted and when responses should stay fast. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can increase token usage and silently change reasoning posture because it is designed as an always-on reasoning preprocessor. <br>
Mitigation: Install it only when automatic reasoning adjustment is desired, and disable it for workflows that require explicit control over reasoning state. <br>
Risk: The skill may add reasoning markers to responses, which can interfere with strict JSON, API, or formatting-sensitive output. <br>
Mitigation: Avoid or disable it for strict structured-output workflows and verify final responses before using them downstream. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cxz9909/cxz9909-adaptive-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Configuration instructions] <br>
**Output Format:** [Markdown guidance with optional response suffix markers and inline command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no code execution, private data access, or external service calls are described by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
