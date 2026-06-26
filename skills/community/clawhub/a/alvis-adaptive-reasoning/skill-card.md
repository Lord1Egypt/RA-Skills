## Description: <br>
Automatically assesses task complexity and adjusts reasoning depth before responding to complex questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers can use this skill to have an agent classify request complexity and decide when to use deeper reasoning for complex, ambiguous, architectural, mathematical, novel, or high-stakes tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automatic reasoning activation can increase token use or reduce explicit user control on complex requests. <br>
Mitigation: Review or edit the activation thresholds before installation when predictable token use or explicit control is required. <br>
Risk: Some threshold rows in the artifact are unclear, which can make activation behavior inconsistent. <br>
Mitigation: Clarify the missing score ranges before relying on the skill for repeatable reasoning-depth decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis-adaptive-reasoning) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, Configuration instructions] <br>
**Output Format:** [Markdown guidance with optional inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompt-only skill; no external tools, files, or network calls are produced by the artifact.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
