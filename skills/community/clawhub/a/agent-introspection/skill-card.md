## Description: <br>
Agent Introspection triggers structured self-reflection at key task points to reduce blind execution, drift, and overconfidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[demo112](https://clawhub.ai/user/demo112) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and agent developers use this skill to pause before important work, decisions, blockage handling, and delivery so they can check assumptions, choose corrective action, and verify behavior changed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Reflection notes may include sensitive task context if written broadly or stored in uncontrolled locations. <br>
Mitigation: Keep reflection notes in a known limited location and avoid including unnecessary sensitive details. <br>
Risk: An agent may treat introspection as permission to take irreversible, external, or high-impact action. <br>
Mitigation: Require human confirmation before irreversible, external, or high-impact actions, including actions suggested during reflection. <br>
Risk: The skill's guidance can be mistaken for completed remediation when it only produces reflection text. <br>
Mitigation: Use the skill's action and verification fields to record a concrete completed action before considering the introspection complete. <br>


## Reference(s): <br>
- [Philosophical Foundations](references/philosophical-foundations.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/demo112/agent-introspection) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown text with structured introspection blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No executable output; reflection should state current status, findings, completed action, and verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
