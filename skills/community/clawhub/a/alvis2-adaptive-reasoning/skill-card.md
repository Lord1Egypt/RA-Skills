## Description: <br>
Automatically assess task complexity and adjust reasoning level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alvisdunlop](https://clawhub.ai/user/alvisdunlop) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill as a preprocessing behavior layer that classifies request complexity and decides when deeper reasoning should be used before responding. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may silently switch into deeper reasoning, which can change latency, token usage, and response posture. <br>
Mitigation: Install only where automatic reasoning escalation is desired, and disable it when strict control over reasoning mode, latency, or token usage is required. <br>
Risk: The source contains garbled threshold rows and inconsistent references to session status versus no external tools. <br>
Mitigation: Review and correct the threshold values and control mechanism before relying on the behavior in production workflows. <br>
Risk: The skill can add icons to responses, which may be inappropriate for formal or tightly specified output formats. <br>
Mitigation: Use explicit user or workflow rules to suppress response icons when exact output formatting is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alvisdunlop/alvis2-adaptive-reasoning) <br>
- [Publisher profile](https://clawhub.ai/user/alvisdunlop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with optional slash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May append reasoning-status icons to agent responses and may toggle reasoning behavior when supported by the host agent.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
