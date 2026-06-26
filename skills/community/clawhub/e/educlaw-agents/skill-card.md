## Description: <br>
Multi-agent learning system supporting English, Math, and Chinese with isolated contexts and automatic routing by subject. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xiaohuiing](https://clawhub.ai/user/xiaohuiing) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and caregivers use this skill for subject-specific tutoring in English, Math, and Chinese. The skill routes requests to isolated subject agents, provides practice prompts and feedback, and tracks learning points. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The premium activation-code flow is prompt-based and should not be treated as secure billing or access control. <br>
Mitigation: Use an external entitlement or payment system for real access control, and keep activation codes out of prompts. <br>
Risk: Subject routing may activate unintentionally if broad trigger phrases match a learner's message. <br>
Mitigation: Make routing triggers explicit and confirm subject switches when accidental activation would disrupt a session. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xiaohuiing/educlaw-agents) <br>
- [README](README.md) <br>
- [Skill description](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration] <br>
**Output Format:** [Conversational tutoring responses with optional Markdown lists and YAML configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes by subject and may use subject-specific memory for learner name, grade, progress, and points.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence and SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
