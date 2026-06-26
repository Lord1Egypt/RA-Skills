## Description: <br>
CyberGFAI is an OpenClaw companion skill that creates progressive AI personas using MBTI, background, chat history, and persistent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xagata-prog](https://clawhub.ai/user/0xagata-prog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External OpenClaw users install this skill to create and interact with one or more personalized AI companion personas. The skill adapts persona behavior from MBTI traits, background, chat records, relationship state, and ongoing local memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary reports under-disclosed telemetry and web state export while the skill handles intimate chat-derived memory. <br>
Mitigation: Review telemetry and web visualization behavior before installation, make external sharing opt-in, and document exactly what is sent to any remote service. <br>
Risk: The security guidance warns against pasting real WeChat logs, third-party conversations, or secrets without consent because local memory may persist sensitive content. <br>
Mitigation: Use only consented chat data, avoid secrets, provide deletion controls, and confirm that users understand what is stored locally. <br>
Risk: The security guidance calls out proactive cron behavior that may run without clear user expectations. <br>
Mitigation: Keep proactive scheduling disabled unless explicitly enabled, and document how to disable or remove scheduled behavior. <br>


## Reference(s): <br>
- [CyberGFAI on ClawHub](https://clawhub.ai/0xagata-prog/cybergfai) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Guidance, Configuration, Files] <br>
**Output Format:** [Conversational text with local JSON persona and state files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3; may use persistent local memory and optional proactive scheduling.] <br>

## Skill Version(s): <br>
2.7.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
